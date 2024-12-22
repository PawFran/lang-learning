import os
from dataclasses import dataclass
from datetime import datetime as dt

from sqlalchemy import func, desc
from toolz import compose

from common.lib.utils import replace_special
from database.db_classes import *
from database.utils import insert_or_ignore
from vocabulary.lib.file_db import TranslationExerciseCSVHandler
from vocabulary.lib.utils import compare_answer_with_full_head_raw

TRANSLATION_EXERCISE_CSV_LOG_FILE = os.path.join('vocabulary', 'db', 'translation_exercise_results.csv')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@dataclass
class SessionMetadata:
    word_count: int
    session_id: int


def start_translation_exercise_session(start_word: str, end_word: str, session: Session) -> SessionMetadata:
    clear_cache_table(session)

    words_for_current_session = get_words_for_current_session(session, start_word=start_word, end_word=end_word)
    new_session_id = get_session_id(session)  # for now only for default user

    # only one user is allowed with current approach
    setup_cache_table(session, words_for_current_session, new_session_id)

    return SessionMetadata(len(words_for_current_session), new_session_id)


def get_session_id(session: Session) -> int:
    old_session_id = session.query(TranslationResults.session_id) \
        .order_by(desc(TranslationResults.session_id)).first()[0]

    new_session_id = 1 if old_session_id is None else old_session_id + 1

    return new_session_id


def random_word_for_cache(session: Session) -> str | None:
    # random translation (ideally with priorities taken into account - but this one is for later)
    # if cache is empty return None
    record = session.query(TranslationExerciseCurrentSession.id, TranslationExerciseCurrentSession.translation) \
        .order_by(func.random()).first()
    if record is not None:
        row_id, word = record[0], record[1]
        session.query(TranslationExerciseCurrentSession).filter_by(id=row_id) \
            .update({TranslationExerciseCurrentSession.is_active: 1})
        session.commit()
        return word
    else:
        return None


def get_words_for_current_session(session, start_word, end_word):
    words = session.query(Words).all()

    base_form = lambda w: w.header.split(',')[0].rstrip()
    base_simple_form = compose(replace_special, base_form)
    simple_word_with_id = lambda w: (w.id, base_simple_form(w))
    bases_simple_form = [simple_word_with_id(w) for w in words]

    start = find_first(bases_simple_form, start_word)
    end = find_first(bases_simple_form, end_word)

    query: text = query_for_start_end(start_id=start[0], end_id=end[0])

    words_for_current_session = session.execute(query).fetchall()

    return words_for_current_session


def setup_cache_table(session: Session, words_for_current_session: [str], new_session_id: int):
    for word in words_for_current_session:
        session.add(TranslationExerciseCurrentSession(
            id=word[0], header=word[1], part_of_speech=word[2],
            translation=word[3], example=word[4], associated_case=word[5],
            session_id=new_session_id)
        )
    session.commit()


def clear_cache_table(session: Session):
    session.query(TranslationExerciseCurrentSession).delete()
    session.commit()


def remove_from_cache(record_id: int, session: Session):
    session.query(TranslationExerciseCurrentSession).filter_by(id=record_id).delete()
    session.commit()


def query_for_start_end(start_id, end_id) -> text:
    if start_id is not None and end_id is not None:
        query = view_words_with_translations_select + f'\nwhere w.id between {start_id} and {end_id}'
    elif end_id is not None:
        query = view_words_with_translations_select + f'\nwhere w.id < {end_id}'
    elif start_id is not None:
        query = view_words_with_translations_select + f'\nwhere w.id > {start_id}'
    else:
        query = view_words_with_translations_select

    return text(query)


def find_first(all_words, word):
    return next((t for t in all_words if t[1] == word), None)


@dataclass
class TranslationFeedback:
    word_id: int
    word_pl: str
    example: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    user_name: str
    session_id: int


def check_translation_answer(answer, session) -> TranslationFeedback:
    # get all active rows
    # check if answer matches any of them (weak equals cannot be easily implemented in sqlalchemy - or maybe it can ?)
    # return ok/nok and correct translation (even if ok for the sake of special characters)
    # save results to csv and db
    result = session.query(TranslationExerciseCurrentSession.header,
                           TranslationExerciseCurrentSession.example,
                           TranslationExerciseCurrentSession.part_of_speech,
                           TranslationExerciseCurrentSession.translation,
                           TranslationExerciseCurrentSession.id,
                           TranslationExerciseCurrentSession.user_name,
                           TranslationExerciseCurrentSession.session_id).filter_by(is_active=1).first()
    correct_answer = result[0]
    example = result[1]
    part_of_speech = result[2]
    word_pl = result[3]
    result_id = result[4]  # for another method to remove this row if necessary
    user_name = result[5]
    session_id = result[6]

    header_with_part_of_speech = correct_answer + f' [{part_of_speech}]'

    verdict = compare_answer_with_full_head_raw(entry_head=header_with_part_of_speech, answer=answer)

    return TranslationFeedback(word_id=result_id, word_pl=word_pl, example=example,
                               user_answer=answer, correct_answer=correct_answer, is_correct=verdict,
                               user_name=user_name, session_id=session_id)


def update_log_csv_file(translation_result: TranslationFeedback, csv_handler: TranslationExerciseCSVHandler):
    csv_handler.update_db(user=DEFAULT_USER_NAME, word_pl=translation_result.word_pl,
                         lang='latin', translation=translation_result.correct_answer,
                         was_correct=translation_result.is_correct, user_answer=translation_result.user_answer)


def update_translation_result_db(feedback: TranslationFeedback, session: Session):
    translation_result = TranslationResults(user=feedback.user_name, session_id=feedback.session_id, lang='latin',
                                            word_pl=feedback.word_pl, expected_answer=feedback.correct_answer,
                                            user_answer=feedback.user_answer, is_correct=feedback.is_correct,
                                            time=dt.now().replace(microsecond=0))

    insert_or_ignore(session, translation_result)
