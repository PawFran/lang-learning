from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.lib.utils import flatten
from database.db_classes import LatinDeclensionPatterns
from database.utils import insert_or_ignore_no_commit
from declension.lib.declension_classes import SingleDeclension, SingleDeclensionPattern, Declensions


def parse_single_declension(declension: SingleDeclension) -> [LatinDeclensionPatterns]:
    return [parse_single_declension_pattern(d) for d in declension.declension_patterns]


def parse_single_declension_pattern(pattern: SingleDeclensionPattern) -> [LatinDeclensionPatterns]:
    singular = [parse_single_declension_row(pattern, 'singular', case, word) for case, word in pattern.singular.items()]
    plural = [parse_single_declension_row(pattern, 'plural', case, word) for case, word in pattern.plural.items()]
    return singular + plural


def replace_genre(s: str) -> str:
    match s.lower().strip():
        case 'femininum':
            return 'feminine'
        case 'masculinum':
            return 'masculine'
        case 'neutrum':
            return 'neutral'
        case '':
            return 'none'
        case _:
            raise ValueError(f'{s} cannot be converted to proper genre')


def parse_single_declension_row(pattern: SingleDeclensionPattern, number: str, case: str,
                                word) -> LatinDeclensionPatterns:
    return LatinDeclensionPatterns(
        base_word=pattern.base_word,
        declension_type=pattern.type.name.replace('_', ' '),
        genre=replace_genre(pattern.genre),
        number=number,
        case=case,
        word=word
    )


def migrate_declension_patterns(engine: Engine, path: str):
    declensions: list[SingleDeclension] = Declensions.from_file_path(path).declensions

    declension_patterns_parsed: [SingleDeclension] = [parse_single_declension(declension) for declension in declensions]

    rows = flatten(flatten(declension_patterns_parsed))

    with Session(engine) as session:
        try:
            for row in rows:
                insert_or_ignore_no_commit(session, row)
            session.commit()
        except IntegrityError as err:
            print(f'cannot insert {row} because of {str(err)}')
