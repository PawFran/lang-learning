import os
import sys
from datetime import datetime

from sqlalchemy import create_engine

from environment import DATABASE

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.utils import *

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_translation_result_line(raw_line: str):
    split = raw_line.split(';')
    return TranslationResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        word_pl=split[3],
        expected_answer=split[4],
        user_answer=split[5],
        is_correct=split[6],
        time=datetime.strptime(split[7].strip(), DATE_FORMAT)
    )


def migrate_translation_results(engine, translation_results_dir: str):
    file_name = 'translation_exercise_results.csv'
    path = os.path.join(translation_results_dir, file_name)
    with open(path, encoding="utf8") as f:
        f.readline()  # skip header
        lines = f.readlines()
    with Session(engine) as session:
        for line in lines:
            translation_result = parse_translation_result_line(line)
            if translation_result is not None:
                insert_or_ignore_no_commit(session, translation_result)
            else:
                print(f'word from line {line} not found')

        session.commit()


if __name__ == '__main__':
    engine = create_engine(DATABASE)
    translation_results_dir = os.path.join('..', 'vocabulary', 'db')
    migrate_translation_results(engine, translation_results_dir)
