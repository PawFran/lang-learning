from sqlalchemy import Engine
from sqlalchemy.orm import Session
from toolz import compose

from common.lib.utils import replace_special
from database.db_classes import *


def start_translation_exercise_session(start_word: str, end_word: str, engine: Engine):
    with Session(engine) as session:
        clear_cache_table(session)

        words_for_current_session = get_words_for_current_session(session, start_word=start_word, end_word=end_word)

        # only one user is allowed with current approach
        insert_words_into_cache_table(session, words_for_current_session)

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


def clear_cache_table(session):
    session.query(TranslationExerciseCurrentSession).delete()
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
