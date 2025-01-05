from datetime import datetime

from sqlalchemy import Engine

from conjugation.lib.conjugation_classes import Number
from database.utils import *
from declension.lib.declension_classes import DeclensionCase

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def str_to_bool(s: str) -> bool:
    match s.lower().strip():
        case 'true':
            return True
        case 'false':
            return False
        case _:
            raise ValueError('''Only 'true' or 'false' strings are acceptable''')


def parse_translation_exercise_result_line(raw_line: str) -> TranslationExerciseResults:
    split = raw_line.split(';')
    return TranslationExerciseResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        word_pl=split[3],
        expected_answer=split[4],
        user_answer=split[5],
        is_correct=str_to_bool(split[6]),
        time=datetime.strptime(split[7].strip(), DATE_FORMAT)
    )


def parse_declension_exercise_result_line(raw_line: str) -> TranslationExerciseResults:
    split = raw_line.split(';')
    return DeclensionExerciseResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        base_word=split[3],
        number=Number.from_string(split[4]).value,
        case=DeclensionCase.from_string(split[5]).value,
        correct_answer=split[6],
        user_answer=split[7],
        is_correct=str_to_bool(split[8]),
        time=datetime.strptime(split[9].strip(), DATE_FORMAT)
    )


def migrate_translation_exercise_results(engine: Engine, path: str):
    migrate_from_file_to_db(engine, path, parse_translation_exercise_result_line)


def migrate_declension_exercise_results(engine: Engine, path: str):
    migrate_from_file_to_db(engine, path, parse_declension_exercise_result_line)


def migrate_from_file_to_db(engine, path: str, parsing_function):
    with open(path, encoding="utf8") as f:
        f.readline()  # skip header
        lines = f.readlines()
    with Session(engine) as session:
        for line in lines:
            try:
                result = parsing_function(line)
                insert_or_ignore_no_commit(session, result)
            except Exception as e:
                print(f'cannot parse {line} because of {str(e)}')

        session.commit()
