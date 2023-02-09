from dataclasses import dataclass
import json


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
    number: str  # int doesn't work for possibilities like 'third consonant' must be allowed
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
            number=number,
            genre=genre,
            singular=DeclensionCasesDict.from_dict(sing_pattern),
            plural=DeclensionCasesDict.from_dict(pl_pattern),
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

        def filter_patterns_by_number(num: str):
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
