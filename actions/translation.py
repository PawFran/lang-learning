from dataclasses import dataclass

from sqlalchemy import func
from sqlalchemy.orm import Session
from toolz import compose

from common.lib.utils import replace_special, weak_equals
from database.db_classes import *
from vocabulary.lib.utils import compare_answer_with_full_head_raw


def start_translation_exercise_session(start_word: str, end_word: str, session: Session):
    clear_cache_table(session)

    words_for_current_session = get_words_for_current_session(session, start_word=start_word, end_word=end_word)

    # only one user is allowed with current approach
    insert_words_into_cache_table(session, words_for_current_session)

    return len(words_for_current_session)


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


def insert_words_into_cache_table(session, words_for_current_session):
    for word in words_for_current_session:
        session.add(TranslationExerciseCurrentSession(
            id=word[0], header=word[1], part_of_speech=word[2],
            translation=word[3], example=word[4], associated_case=word[5]))
    session.commit()


def clear_cache_table(session: Session):
    session.query(TranslationExerciseCurrentSession).delete()
    session.commit()


def remove_from_cache(record_id: int, session: Session):
    session.query(TranslationExerciseCurrentSession).filter(id=record_id).delete()
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
    is_correct: bool
    user_answer: str
    correct_answer: str
    example: str
    word_id: int


def check_translation_answer(answer, session) -> TranslationFeedback:
    # get all active rows
    # check if answer matches any of them (weak equals cannot be easily implemented in sqlalchemy - or maybe it can ?)
    # return ok/nok and correct translation (even if ok for the sake of special characters)
    result = session.query(TranslationExerciseCurrentSession.header,
                           TranslationExerciseCurrentSession.example,
                           TranslationExerciseCurrentSession.id).filter_by(is_active=1).first()
    correct_answer = result[0]
    example = result[1]
    result_id = result[2] # for another method to remove this row if necessary

    verdict = compare_answer_with_full_head_raw(entry_head=correct_answer, answer=answer)

    return TranslationFeedback(is_correct=verdict, user_answer=answer, correct_answer=correct_answer, example=example,
                               word_id=result_id)
