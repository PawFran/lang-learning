import json
from dataclasses import dataclass
from enum import Enum


class DeclensionType(Enum):
    I = 1
    II = 2
    III = 3
    III_consonant = 3.1
    III_vowel = 3.2
    III_mixed = 3.3
    IV = 4
    V = 5

    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').strip():
            case 'first' | 'i' | 'one' | '1':
                return DeclensionType.I
            case 'second' | 'ii' | 'two' | '2':
                return DeclensionType.II
            case 'third' | 'iii' | 'three' | '3':
                return DeclensionType.III
            case 'third consonant' | 'iii consonant' | 'three consonant' | '3 consonant':
                return DeclensionType.III_consonant
            case 'third vowel' | 'iii vowel' | 'three vowel' | '3 vowel':
                return DeclensionType.III_vowel
            case 'third mixed' | 'iii mixed' | 'three mixed' | '3 mixed':
                return DeclensionType.III_mixed
            case 'fourth' | 'iv' | 'four' | '4':
                return DeclensionType.IV
            case 'fifth' | 'v' | 'five' | '5':
                return DeclensionType.V
            case _:
                raise Exception(f'cannot parse string {s} to DeclensionNumber')


class DeclensionCase(Enum):
    NOMINATIVUS = 1
    GENETIVUS = 2
    DATIVUS = 3
    ACCUSATIVUS = 4
    ABLATIVUS = 5
    VOCATIVUS = 6

    @staticmethod
    def from_string(s: str):
        match s.lower().strip():
            case 'nominativus' | 'nominative' | 'nom':
                return DeclensionCase.NOMINATIVUS
            case 'genetivus' | 'genetive' | 'gen':
                return DeclensionCase.GENETIVUS
            case 'dativus' | 'dative' | 'dat':
                return DeclensionCase.DATIVUS
            case 'accusativus' | 'accusative' | 'acc':
                return DeclensionCase.ACCUSATIVUS
            case 'ablativus' | 'ablative' | 'abl':
                return DeclensionCase.ABLATIVUS
            case 'vocativus' | 'vocative' | 'voc':
                return DeclensionCase.VOCATIVUS
            case _:
                raise Exception(f'cannot parse {s} to DeclensionCase')

    # todo remove it ?
    @staticmethod
    def to_string(c):
        match c:
            case DeclensionCase.NOMINATIVUS:
                return "nominativus"
            case DeclensionCase.GENETIVUS:
                return "genetivus"
            case DeclensionCase.DATIVUS:
                return "dativus"
            case DeclensionCase.ACCUSATIVUS:
                return "accusativus"
            case DeclensionCase.ABLATIVUS:
                return "nominativus"
            case DeclensionCase.VOCATIVUS:
                return "nominativus"
            case _:
                raise Exception(f'cannot parse {c} to case string representation')


# todo probably get rid off it and use simple dictionary
# @dataclass
# class DeclensionCasesDict:
#     nominativus: str
#     genetivus: str
#     dativus: str
#     accusativus: str
#     ablativus: str
#     vocativus: str
#
#     @staticmethod
#     def from_dict(d):
#         return DeclensionCasesDict(
#             d['nominativus'],
#             d['genetivus'],
#             d['dativus'],
#             d['accusativus'],
#             d['ablativus'],
#             d['vocativus']
#         )
#
#     @staticmethod
#     def to_dict():
#         return {
#             'nominativus': DeclensionCasesDict.NOMINATIVUS,
#             'genetivus': DeclensionCasesDict.GENETIVUS,
#             'dativus': DeclensionCasesDict.DATIVUS,
#             'accusativus': DeclensionCasesDict.ACCUSATIVUS,
#             'ablativus': DeclensionCasesDict.ABLATIVUS,
#             'vocativus': DeclensionCasesDict.VOCATIVUS
#         }


# todo single pattern should be ONE of [singular, plural]
#  another class will be necessary with number enum possibly
@dataclass
class SingleDeclensionPattern:
    # DeclensionPattern should be uniquely identified by either base_word or (number, genre)
    base_word: str
    type: DeclensionType
    genre: str
    singular: dict
    plural: dict

    def get_word(self, case, singular: bool):
        cases_dict = self.singular if singular else self.plural
        # cases_dict

    @staticmethod
    def from_dict(d: dict):
        base_word = [*d][0]
        number = [*d[base_word]][0]
        genre = [*d[base_word][number]][0]

        sing_pattern = d[base_word][number][genre]['singularis']
        pl_pattern = d[base_word][number][genre]['pluralis']

        return SingleDeclensionPattern(
            base_word=base_word,
            type=DeclensionType.from_string(number),
            genre=genre,
            singular=sing_pattern,
            plural=pl_pattern
        )


@dataclass
class SingleDeclension:
    # for a few declensions (ex. second, third) multiple variants are possible (ex. different patterns for masculinum and neutrum)
    type: DeclensionType
    declension_patterns: list[SingleDeclensionPattern]
    # optionally some short description like when it's used. where to put it ? probably not in description because it would be duplicated


@dataclass
class Declensions:
    declensions: list[SingleDeclension]

    # todo tests
    @staticmethod
    def _group_declension_patterns_by_numbers(patterns: list[SingleDeclensionPattern]):
        all_numbers = set([p.type for p in patterns])

        def filter_patterns_by_number(num: DeclensionType):
            return [p for p in patterns if p.type == num]

        return {num: filter_patterns_by_number(num)
                for num in all_numbers}

    # todo tests
    @staticmethod
    def _from_dict(d: dict):
        declension_patterns = [SingleDeclensionPattern.from_dict({base_word: d[base_word]})
                               for base_word in [*d]]

        declensions_grouped_dict = Declensions._group_declension_patterns_by_numbers(declension_patterns)
        declensions_list = [SingleDeclension(number, pattern) for number, pattern in declensions_grouped_dict.items()]

        return Declensions(declensions_list)

    @staticmethod
    def from_file_path(json_file_path):
        with open(json_file_path) as f:
            d = json.load(f)
            return Declensions._from_dict(d)

    # todo tests
    def nth(self, num: str):
        # only one Declension instance for given number (but multiple patterns) possible
        return [dec for dec in self.declensions if dec.type == num][0]
