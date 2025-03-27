from datetime import datetime

from sqlalchemy import Engine

from conjugation.lib.conjugation_classes import Number, Mood, Tense, Voice, Person
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
    split = [field.strip() for field in raw_line.split(';')]
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


def parse_reversed_translation_exercise_result_line(raw_line: str) -> ReversedTranslationExerciseResults:
    split = [field.strip() for field in raw_line.split(';')]
    return ReversedTranslationExerciseResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        word_asked=split[3],
        example=split[4],
        translation_total_number=split[5],
        translations_left=split[6],
        user_answer=split[7],
        is_correct=str_to_bool(split[8]),
        time=datetime.strptime(split[9].strip(), DATE_FORMAT)
    )


def parse_declension_exercise_result_line(raw_line: str) -> DeclensionExerciseResults:
    split = [field.strip() for field in raw_line.split(';')]
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


def parse_conjugation_exercise_result_line(raw_line: str) -> TranslationExerciseResults:
    split = [field.strip() for field in raw_line.split(';')]
    return ConjugationExerciseResults(
        user=split[0],
        session_id=split[1],
        lang=split[2],
        infinitive=split[3],
        mood=Mood.from_string(split[4]).value,
        tense=Tense.from_string(split[5]).value,
        voice=Voice.from_string(split[6]).value,
        person=Person.from_string(split[7]).value,
        number=Number.from_string(split[8]).value,
        correct_answer=split[9],
        user_answer=split[10],
        is_correct=str_to_bool(split[11]),
        time=datetime.strptime(split[12].strip(), DATE_FORMAT)
    )


def migrate_translation_exercise_results(engine: Engine, path: str):
    migrate_from_file_to_db(engine, path, parse_translation_exercise_result_line)


def migrate_reversed_translation_exercise_results(engine: Engine, path: str):
    migrate_from_file_to_db(engine, path, parse_reversed_translation_exercise_result_line)


def migrate_declension_exercise_results(engine: Engine, path: str):
    migrate_from_file_to_db(engine, path, parse_declension_exercise_result_line)


def migrate_conjugation_exercise_results(engine: Engine, path: str):
    migrate_from_file_to_db(engine, path, parse_conjugation_exercise_result_line)


def migrate_declension_exercise_session_metadata(engine: Engine, path: str):
    def parse_declension_session_metadata_line(raw_line: str) -> DeclensionExerciseSessionMetadata:
        split = [field.strip() for field in raw_line.split(';')]
        return DeclensionExerciseSessionMetadata(
            session_id=split[0],
            user_name=split[1],
            declensions_included=split[2],
            interrupted=str_to_bool(split[3].strip())
        )

    migrate_from_file_to_db(engine, path, parse_declension_session_metadata_line)


def migrate_translation_exercise_session_metadata(engine: Engine, path: str):
    def parse_translation_session_metadata_line(raw_line: str) -> TranslationExerciseSessionMetadata:
        split = [field.strip() for field in raw_line.split(';')]
        return TranslationExerciseSessionMetadata(
            session_id=split[0],
            user_name=split[1],
            start_word=split[2],
            end_word=split[3],
            filtered_parts_of_speech=split[4],
            revise_last_session=str_to_bool(split[5].strip()),
            interrupted=str_to_bool(split[6].strip())
        )

    migrate_from_file_to_db(engine, path, parse_translation_session_metadata_line)


def migrate_reversed_translation_exercise_session_metadata(engine: Engine, path: str):
    def parse_reversed_translation_session_metadata_line(raw_line: str) -> ReversedTranslationExerciseSessionMetadata:
        split = [field.strip() for field in raw_line.split(';')]
        return ReversedTranslationExerciseSessionMetadata(
            session_id=split[0],
            user_name=split[1],
            start_word=split[2],
            end_word=split[3],
            filtered_parts_of_speech=split[4],
            revise_last_session=str_to_bool(split[5].strip()),
            interrupted=str_to_bool(split[6].strip())
        )

    migrate_from_file_to_db(engine, path, parse_reversed_translation_session_metadata_line)


def migrate_conjugation_exercise_session_metadata(engine: Engine, path: str):
    def parse_conjugation_session_metadata_line(raw_line: str) -> ConjugationExerciseSessionMetadata:
        split = [field.strip() for field in raw_line.split(';')]
        return ConjugationExerciseSessionMetadata(
            session_id=split[0],
            user_name=split[1],
            conjugations_included=split[2],
            moods_included=split[3],
            tenses_included=split[4],
            voices_included=split[5],
            interrupted=str_to_bool(split[6].strip())
        )

    migrate_from_file_to_db(engine, path, parse_conjugation_session_metadata_line)

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
