from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.lib.utils import flatten
from conjugation.lib.conjugation_classes import ConjugationTable, SingleConjugationRecord
from database.db_classes import LatinDeclensionPatterns, LatinConjugationPatterns
from database.utils import insert_or_ignore_no_commit
from declension.lib.declension_classes import SingleDeclension, SingleDeclensionPattern, Declensions, Genre, \
    DeclensionCase


def parse_single_declension(declension: SingleDeclension) -> [LatinDeclensionPatterns]:
    return [parse_single_declension_pattern(d) for d in declension.declension_patterns]


def parse_single_declension_pattern(pattern: SingleDeclensionPattern) -> [LatinDeclensionPatterns]:
    singular = [parse_single_declension_row(pattern, 'singular', case, word) for case, word in pattern.singular.items()]
    plural = [parse_single_declension_row(pattern, 'plural', case, word) for case, word in pattern.plural.items()]
    return singular + plural


def parse_single_declension_row(pattern: SingleDeclensionPattern, number: str, case: str,
                                word) -> LatinDeclensionPatterns:
    return LatinDeclensionPatterns(
        base_word=pattern.base_word,
        declension_type=pattern.type.value,
        genre=Genre.from_string(pattern.genre).value,
        number=number,
        case=DeclensionCase.from_string(case).value,
        word=word
    )


def migrate_declension_patterns(engine: Engine, path: str):
    declensions: list[SingleDeclension] = Declensions.from_file_path(path).declensions

    declension_patterns_parsed: [SingleDeclension] = [parse_single_declension(declension) for declension in declensions]

    rows = flatten(flatten(declension_patterns_parsed))
# [row for row in rows if 'demonstrative' in row.declension_type]
    with Session(engine) as session:
        try:
            for row in rows:
                insert_or_ignore_no_commit(session, row)
            session.commit()
        except IntegrityError as err:
            print(f'cannot insert {row} because of {str(err)}')


def parse_single_conjugation_pattern_record(x: SingleConjugationRecord) -> LatinConjugationPatterns:
    return LatinConjugationPatterns(
        infinitive=x.infinitive,
        conjugation_type=x.conjugation_type.value,
        mood=x.mood.value,
        tense=x.tense.value,
        voice=x.voice.value,
        number=x.number.value,
        person=x.person.value,
        word=x.word
    )


def migrate_conjugation_patterns(engine: Engine, path: str):
    conjugation_all_table: list[SingleConjugationRecord] = ConjugationTable.from_file_path(path).records

    rows: list[LatinConjugationPatterns] = [parse_single_conjugation_pattern_record(x) for x in conjugation_all_table]

    with Session(engine) as session:
        try:
            for row in rows:
                insert_or_ignore_no_commit(session, row)
            session.commit()
        except IntegrityError as err:
            print(f'cannot insert {row} because of {str(err)}')
