from utils import *
from sqlalchemy import create_engine
from datetime import datetime


def parse_translation_result_line(raw_line: str):
    split = raw_line.split(';')
    date_format = "%Y-%m-%d %H:%M:%S"
    return TranslationResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        word_pl=split[3],
        correct_translation=split[4],
        user_answer=split[5],
        is_correct=split[6],
        time=datetime.strptime(split[7].strip(), date_format)
    )


def migrate_translation_results():
    file_name = 'translation_exercise_results.csv'
    path = os.path.join('..', 'vocabulary', 'db', file_name)
    with open(path, encoding="utf8") as f:
        f.readline()  # skip header
        lines = f.readlines()
    engine = create_engine('sqlite:///lang_learning.sqlite')
    with Session(engine) as session:
        for line in lines:
            translation_result = parse_translation_result_line(line)
            insert_or_ignore(session, translation_result)

        session.commit()


if __name__ == '__main__':
    migrate_translation_results()
