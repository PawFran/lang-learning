import json
from dataclasses import dataclass
from enum import Enum


class DeclensionNumber(Enum):
    I = 1
    II = 2
    III_consonant = 3.1
    III_vowel = 3.2
    III_mixed = 3.3
    IV = 4
    V = 5

    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').strip():
            case 'first' | 'i' | 'one' | '1':
                return DeclensionNumber.I
            case 'second' | 'ii' | 'two' | '2':
                return DeclensionNumber.II
            case 'third consonant' | 'iii consonant' | 'three consonant' | '3 consonant':
                return DeclensionNumber.III_consonant
            case 'third vowel' | 'iii vowel' | 'three vowel' | '3 vowel':
                return DeclensionNumber.III_vowel
            case 'third mixed' | 'iii mixed' | 'three mixed' | '3 mixed':
                return DeclensionNumber.III_mixed
            case 'fourth' | 'iv' | 'four' | '4':
                return DeclensionNumber.IV
            case 'fifth' | 'v' | 'five' | '5':
                return DeclensionNumber.V
            case _:
                raise Exception(f'cannot parse string {s} to DeclensionNumber')

# todo declension cases enum ?
# todo declension genre enum ?
# todo declension sing/pl enum ?

@dataclass
class DeclensionCasesDict:
    nominativus: str
    genetivus: str
    dativus: str
    accusativus: str
    ablativus: str
    vocativus: str

    @staticmethod
    def from_dict(d):
        return DeclensionCasesDict(
            d['nominativus'],
            d['genetivus'],
            d['dativus'],
            d['accusativus'],
            d['ablativus'],
            d['vocativus']
        )


@dataclass
class SingleDeclensionPattern:
    # DeclensionPattern should be uniquely identified by either base_word or (number, genre)
    base_word: str
    number: DeclensionNumber
    genre: str
    singular: DeclensionCasesDict
    plural: DeclensionCasesDict

    @staticmethod
    def from_dict(d: dict):
        base_word = [*d][0]
        number = [*d[base_word]][0]
        genre = [*d[base_word][number]][0]

        sing_pattern = d[base_word][number][genre]['singularis']
        pl_pattern = d[base_word][number][genre]['pluralis']

        return SingleDeclensionPattern(
            base_word=base_word,
            number=DeclensionNumber.from_string(number),
            genre=genre,
            singular=DeclensionCasesDict.from_dict(sing_pattern),
            plural=DeclensionCasesDict.from_dict(pl_pattern)
        )


@dataclass
class Declension:
    # for a few declensions (ex. second, third) multiple variants are possible (ex. different patterns for masculinum and neutrum)
    number: str
    declension_patterns: list[SingleDeclensionPattern]
    # optionally some short description like when it's used. where to put it ? probably not in description because it would be duplicated


@dataclass
class DeclensionDict:
    declensions: list[Declension]

    # todo tests
    @staticmethod
    def _group_declension_patterns_by_numbers(patterns: list[SingleDeclensionPattern]):
        all_numbers = set([p.number for p in patterns])

        def filter_patterns_by_number(num: DeclensionNumber):
            return [p for p in patterns if p.number == num]

        return {num: filter_patterns_by_number(num)
                for num in all_numbers}

    # todo tests
    @staticmethod
    def _from_dict(d: dict):
        declension_patterns = [SingleDeclensionPattern.from_dict({base_word: d[base_word]})
                               for base_word in [*d]]

        declensions_grouped_dict = DeclensionDict._group_declension_patterns_by_numbers(declension_patterns)
        declensions_list = [Declension(number, pattern) for number, pattern in declensions_grouped_dict.items()]

        return DeclensionDict(declensions_list)

    @staticmethod
    def from_file_path(json_file_path):
        with open(json_file_path) as f:
            d = json.load(f)
            return DeclensionDict._from_dict(d)

    # todo tests
    def nth(self, num: str):
        # only one Declension instance for given number (but multiple patterns) possible
        return [dec for dec in self.declensions if dec.number == num][0]
