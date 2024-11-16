import os

from sqlalchemy.orm import Session

from db_classes import TranslationResult, engine
from utils import insert_or_ignore


def parse_translation_result_line(raw_line: str):
    split = raw_line.split(';')
    return TranslationResult(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        word_pl=split[3],
        correct_translation=split[4],
        user_answer=split[5],
        is_correct=split[6],
        time=split[7]
    )


if __name__ == '__main__':
    file_name = 'translation_exercise_results.csv'
    path = os.path.join('..', 'vocabulary', 'db', file_name)

    with open(path, encoding="utf8") as f:
        f.readline()  # skip header
        lines = f.readlines()

    with Session(engine) as session:
        for line in lines:
            translation_result = parse_translation_result_line(line)
            insert_or_ignore(session, translation_result)

        session.commit()
