import os
import shutil

import pytest

from vocabulary.lib.db import *

folder = os.path.join('vocabulary', 'test', 'resources')

# to avoid editing original test file temporary file will be created for tests
original_file_name = 'test_translation_exercise_results.csv'
temporary_test_file = 'tmp.csv'

original_path = os.path.join(folder, original_file_name)
temporary_path = os.path.join(folder, temporary_test_file)

db_handler = TranslationExerciseDBHandler(temporary_path)


def setup():
    shutil.copyfile(original_path, temporary_path)


def cleanup():
    os.remove(temporary_path)


def test_get():
    df = db_handler.get()

    assert len(df.index) == 4
    assert df.user[0] == 'pf'
    assert df.word_pl[0] == 'winnica'
    assert df.lang[0] == 'latin'
    assert df.translation[0] == 'vinea'
    assert df.correct[0]
    assert df.last_check[0] == dt.strptime('2023-04-20 12:13:00', datetime_format)


def test_add_record():
    setup()

    new_user = 'test_user'
    new_word = 'rarus'
    translation = 'rzadki, mało kto'
    lang = 'latin'
    was_correct = False

    db_handler.update_db(new_user, new_word, lang, translation, was_correct=was_correct)

    df = db_handler.get()

    # cleanup before assertions
    cleanup()

    assert len(df.index) == 5
    assert df.user[4] == new_user
    assert df.word_pl[4] == new_word
    assert df.lang[4] == lang
    assert df.translation[4] == translation
    assert df.correct[4] == was_correct
    assert (dt.now() - df.last_check[4]).seconds < 30


@pytest.mark.skip(reason='not used now')
def test_update_record_correct_answer():
    setup()

    user = 'pf'
    word_pl = 'budynek'
    translation = 'aedeficium'
    lang = 'latin'

    db_handler.update_db(user, word_pl, lang, translation, was_correct=True)

    df = db_handler.get()

    cleanup()

    assert len(df.index) == 2
    assert df.user[1] == user
    assert df.word_pl[1] == word_pl
    assert df.lang[1] == lang
    assert df.translation[1] == translation
    assert df.correct[1] == 3
    assert df.wrong[1] == 1
    assert (dt.now() - df.last_check[1]).seconds < 30


@pytest.mark.skip(reason='not used now')
def test_update_record_wrong_answer():
    setup()

    user = 'pf'
    word = 'winnica'
    translation = 'vinea'
    lang = 'latin'

    db_handler.update_db(user, word, lang, translation, was_correct=False)

    df = db_handler.get()

    cleanup()

    assert len(df.index) == 2
    assert df.user[0] == user
    assert df.word_pl[0] == word
    assert df.lang[0] == lang
    assert df.translation[0] == translation
    assert df.correct[0] == 2
    assert df.wrong[0] == 2
    assert (dt.now() - df.last_check[0]).seconds < 30
