import os
import sys
from datetime import datetime

from sqlalchemy import Engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.utils import *

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def str_to_bool(s: str) -> bool:
    match s.lower().strip():
        case 'true':
            return True
        case 'false':
            return False
        case _:
            raise ValueError('''Only 'true' or 'false' strings are acceptable''')


def parse_translation_result_line(raw_line: str):
    split = raw_line.split(';')
    return TranslationResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        word_pl=split[3],
        expected_answer=split[4],
        user_answer=split[5],
        is_correct=str_to_bool(split[6]),
        time=datetime.strptime(split[7].strip(), DATE_FORMAT)
    )


def migrate_translation_results(engine: Engine, path: str):
    message = lambda line: f'word from line {line} not found'

    migrate(engine, path, parse_translation_result_line, message)


def migrate(engine, path: str, parsing_function, error_message):
    # to use string interpolation error message should be function str -> str
    with open(path, encoding="utf8") as f:
        f.readline()  # skip header
        lines = f.readlines()
    with Session(engine) as session:
        for line in lines:
            result = parsing_function(line)
            if result is not None:
                insert_or_ignore_no_commit(session, result)
            else:
                print(error_message)

        session.commit()
