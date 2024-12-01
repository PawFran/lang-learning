from datetime import datetime

from sqlalchemy import create_engine

from utils import *

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


def migrate_translation_results(engine):
    file_name = 'translation_exercise_results.csv'
    path = os.path.join('..', 'vocabulary', 'db', file_name)
    with open(path, encoding="utf8") as f:
        f.readline()  # skip header
        lines = f.readlines()
    with Session(engine) as session:
        for line in lines:
            translation_result = parse_translation_result_line(line)
            if translation_result is not None:
                insert_or_ignore(session, translation_result)
            else:
                print(f'word from line {line} not found')

        session.commit()


if __name__ == '__main__':
    engine = create_engine(DATABASE)
    migrate_translation_results(engine)
