import json
from dataclasses import dataclass
from enum import Enum

from common.lib.utils import flatten, weak_in


class DeclensionType(Enum):
    I = 'I'
    II = 'II'
    III = 'III'
    III_consonant = 'III consonant'
    III_vowel = 'III vowel'
    III_mixed = 'III mixed'
    IV = 'IV'
    V = 'V'
    relative = 'relative'
    demonstrative = 'demonstrative'  # to be deleted ?
    demonstrative_is_ea_id = 'demonstrative (is, ea, id)'
    demonstrative_hic_haec_hoc = 'demonstrative (hic, haec, hoc)'
    demonstrative_ille_illa_illud = 'demonstrative (ille, illa, illud)'
    demonstrative_idem_eadem_idem = 'demonstrative (idem, eadem, idem)'
    interrogative = 'interrogative'

    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ').replace(',',
                                                                                                        ' ').replace(
            '  ', ' ').strip():
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
            case 'relative' | 'rel':
                return DeclensionType.relative
            case 'demonstrative' | 'dem':
                return DeclensionType.demonstrative
            case 'demonstrative is ea id' | 'dem is ea id' | 'is ea id' | 'is':
                return DeclensionType.demonstrative_is_ea_id
            case 'demonstrative hic haec hoc' | 'dem hic haec hoc' | 'hic haec hoc' | 'hic':
                return DeclensionType.demonstrative_hic_haec_hoc
            case 'demonstrative ille illa illud' | 'dem ille illa illud' | 'ille illa illud' | 'ille':
                return DeclensionType.demonstrative_ille_illa_illud
            case 'demonstrative idem eadem idem' | 'dem idem eadem idem' | 'idem eadem idem' | 'idem':
                return DeclensionType.demonstrative_idem_eadem_idem
            case 'interrogative' | 'inter':
                return DeclensionType.interrogative
            case _:
                raise Exception(f'cannot parse string {s} to DeclensionType')


class DeclensionCase(Enum):
    NOMINATIVUS = 'nominative'
    GENETIVUS = 'genitive'
    DATIVUS = 'dative'
    ACCUSATIVUS = 'accusative'
    ABLATIVUS = 'ablative'
    VOCATIVUS = 'vocative'

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


class Genre(Enum):
    MASCULINE = 'masculine'
    FEMININE = 'feminine'
    NEUTRAL = 'neutral'
    MASCULINE_AND_FEMININE = 'masculine and feminine'
    NONE = 'none'

    @staticmethod
    def from_string(s):
        match s.lower().strip():
            case 'femininum' | 'f':
                return Genre.FEMININE
            case 'masculinum' | 'm':
                return Genre.MASCULINE
            case 'neutrum' | 'n':
                return Genre.NEUTRAL
            case 'm/f':
                return Genre.MASCULINE_AND_FEMININE
            case '' | None:
                return Genre.NONE
            case _:
                raise ValueError(f'{s} cannot be converted to proper genre')


class GrammaticalCase(Enum):
    NOMINATIVE = 'nom'
    GENITIVE = 'gen'
    DATIVE = 'dat'
    ACCUSATIVE = 'acc'
    ABLATIVE = 'abl'
    VOCATIVE = 'voc'

    @staticmethod
    def from_string(s):
        match s.lower.strip():
            case 'nom' | 'nominativus' | 'nominative':
                return GrammaticalCase.NOMINATIVE
            case 'gen' | 'genetivus' | 'genitive':
                return GrammaticalCase.GENITIVE
            case 'dat' | 'dativus' | 'dative':
                return GrammaticalCase.DATIVE
            case 'acc' | 'accusativus' | 'accusative':
                return GrammaticalCase.ACCUSATIVE
            case 'abl' | 'ablativus' | 'ablative':
                return GrammaticalCase.ABLATIVE
            case 'voc' | 'vocativus' | 'vocative':
                return GrammaticalCase.VOCATIVE


@dataclass
class DeclensionPrompt:
    base_word: str
    number: str
    case: str


@dataclass
class DeclensionTest:
    prompt: DeclensionPrompt
    answer: str


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

    @staticmethod
    def from_dict(d: dict):
        base_word = [*d][0]
        number = [*d[base_word]][0]
        genre = [*d[base_word][number]][0]

        word_nr_genre = d[base_word][number][genre]

        sing_pattern = word_nr_genre['singularis']
        pl_pattern = {}
        # some pronouns doesn't have plural
        if len(word_nr_genre.keys()) > 1:
            pl_pattern = word_nr_genre['pluralis']

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
        with open(json_file_path, encoding="utf8") as f:
            d = json.load(f)
            return Declensions._from_dict(d)

    # todo tests
    def nth(self, num: str):
        # only one Declension instance for given number (but multiple patterns) possible
        return [dec for dec in self.declensions if dec.type == num][0]

    def length(self):
        patterns_all: list[SingleDeclensionPattern] = flatten(
            [x.declension_patterns for x in self.declensions]
        )

        cnt = 0
        for pattern in patterns_all:
            cnt += len(pattern.plural) + len(pattern.singular)

        return cnt

    def filter_by_base_words(self, words: list[str]) -> 'Declensions':
        filtered_declensions = []
        for declension in self.declensions:
            filtered_patterns = [pattern for pattern in declension.declension_patterns
                                 if weak_in(pattern.base_word, words)]
            if filtered_patterns:
                filtered_declensions.append(SingleDeclension(
                    type=declension.type,
                    declension_patterns=filtered_patterns
                ))
        return Declensions(filtered_declensions)
