from dataclasses import dataclass

import numpy as np
from numpy.random import default_rng

from common.lib.utils import flatten
from common.lib.utils import weak_equals
from vocabulary.lib.db import *
import re
from conjugation.lib.conjugation_classes import ConjugationType


@dataclass
class AbstractWord:
    base: str
    head_raw: str

    # todo abstract static method from_entry head ?

    @staticmethod
    def extract_from_square_brackets(pattern, line):
        match = re.search(pattern, line)
        if match is not None:
            return match.group().replace('[', '').replace(']',
                                                          '')  # should be possible by using some groups in re directly ?
        else:
            return None

    @staticmethod
    def extract_metadata(head):
        pattern = r'\[.*?\]'
        res_including_brackets = re.findall(pattern, head)
        res_excluding_brackets = [x.replace('[', '').replace(']', '') for x in res_including_brackets]

        return res_excluding_brackets


@dataclass
class LatinVerb(AbstractWord):
    infinite: str
    perfect: str
    supine: str
    conjugation: ConjugationType

    @staticmethod
    def is_verb(dict_entry_head):
        return '[verb]' in dict_entry_head.lower()

    @staticmethod
    def which_conjugation(dict_entry_head) -> ConjugationType:
        # conjugation may be [I] or [II] or [III] or [IIIa] or [IV]
        conjugation_pattern = '\[I{1,3}V*\]|\[anomalous\]|\[anomaly\]|\[anom\]'
        extracted_str = AbstractWord.extract_from_square_brackets(conjugation_pattern, dict_entry_head)
        if extracted_str is None:
            raise Exception(f'cannot extract ConjugationType from {dict_entry_head} using pattern {conjugation_pattern}')
        else:
            return ConjugationType.from_string(extracted_str)

    @staticmethod
    def from_entry_head(head):
        split = head.split(',')

        def get_nth(word_split, n):
            return word_split[n].strip().split(' ')[0].strip()

        def get_supine(word_split):
            return get_nth(word_split, 3) if len(word_split) > 3 else None

        return LatinVerb(
            base=split[0].strip(),
            head_raw=head,
            infinite=get_nth(split, 1),
            perfect=get_nth(split, 2),
            supine=get_supine(split),
            conjugation=LatinVerb.which_conjugation(head)
        )


@dataclass
class LatinNoun(AbstractWord):
    genetive: str
    genre: str
    only_plural: bool
    declension: str  # roman number

    @staticmethod
    def is_noun(dict_entry_head):
        return '[noun]' in dict_entry_head.lower()

    @staticmethod
    def is_only_plural(dict_entry_head):
        return '[pl]' in dict_entry_head.lower()

    @staticmethod
    def which_declension(dict_entry_head):
        # declension may be [I] or [II] or [III vowel] or [III consonant] or [III mixed] or [IV] or [V]
        declension_pattern = '\[I{0,3} *(vowel)*(consonant)*(mixed)*V*\]'
        return AbstractWord.extract_from_square_brackets(declension_pattern, dict_entry_head)

    @staticmethod
    def which_genre(dict_entry_head):
        genre_pattern = '\[[fmn]\]'
        return AbstractWord.extract_from_square_brackets(genre_pattern, dict_entry_head)

    @staticmethod
    def from_entry_head(head):
        split = head.split(',')
        return LatinNoun(
            base=split[0].strip(),
            head_raw=head,
            genetive=split[1].strip().split(' ')[0].strip(),
            genre=LatinNoun.which_genre(head),
            only_plural=LatinNoun.is_only_plural(head),
            declension=LatinNoun.which_declension(head)
        )


@dataclass
class LatinAdverb(AbstractWord):

    @staticmethod
    def is_adverb(dict_entry_head):
        return '[adv]' in dict_entry_head.lower()

    @staticmethod
    def from_entry_head(head):
        return LatinAdverb(
            base=head.split(' ')[0],
            head_raw=head
        )


@dataclass
class LatinPreposition(AbstractWord):

    @staticmethod
    def is_preposition(dict_entry_head):
        return '[prep]' in dict_entry_head.lower()

    @staticmethod
    def from_entry_head(head):
        return LatinAdverb(
            base=head.split(' ')[0],
            head_raw=head
        )


@dataclass
class LatinConjunction(AbstractWord):

    @staticmethod
    def is_conjunction(dict_entry_head):
        return '[conj]' in dict_entry_head.lower()

    @staticmethod
    def from_entry_head(head):
        return LatinConjunction(
            base=head.split(' ')[0],
            head_raw=head
        )


@dataclass
class LatinAdjective(AbstractWord):
    femininum: str
    neutrum: str

    @staticmethod
    def is_adjective(dict_entry_head):
        return '[adj]' in dict_entry_head.lower()

    @staticmethod
    def from_entry_head(head):
        split = head.split(',')
        return LatinAdjective(
            base=split[0],
            head_raw=head,
            femininum=split[1].strip(),
            neutrum=split[2].strip().split(' ')[0]
        )


@dataclass
class EnglishWord(AbstractWord):  # all english dict entries have the same structure, unlike in latin
    part_of_speech: str

    @staticmethod
    def which_part_of_speech(dict_entry_head):
        pattern = 'verb|idiom|noun|adj|adv|phrasal verb'
        return AbstractWord.extract_from_square_brackets(pattern, dict_entry_head.lower())

    @staticmethod
    def from_entry_head(head):
        head_before_brackets = head.strip().split('[')[0].strip()
        return EnglishWord(
            base=head_before_brackets,
            head_raw=head,
            part_of_speech=EnglishWord.which_part_of_speech(head)
        )


@dataclass
class DictionaryEntry:
    """storing entries like:
    castīgo, castīgāre, castīgāvi, castīgātum [verb] [I]
    (Ancillam miseram domina sevēra castīgat)
    1. karać
    """
    head: AbstractWord  # basic dictionary entry that is base word with another info like in above example
    example: str
    translations: list[str]


@dataclass
class DictEntryWithSingleTranslationHighlighted:
    entry: DictionaryEntry
    translation: str


class Dictionary:
    """full dictionary"""

    def __init__(self, entries: list[DictionaryEntry], lang: str):
        self.entries = entries
        self.lang = lang

    def append(self, dict_entry):
        self.entries.append(dict_entry)

    def remove_entry(self, dict_entry):
        self.entries.remove(dict_entry)

    def filter_by_simple_condition(self, metadata: list[str]):
        """
        :param metadata: ex. verb I etc.
        :return: subset of dict containing entries fulfilling selected criteria
        """

        def simplified(xs: [str]):
            return [x.lower().strip() for x in xs]

        metadata_processed = simplified(metadata)

        res_dict = Dictionary(entries=[], lang=self.lang)
        for entry in self.entries:
            head = entry.head.head_raw
            word_metadata: [str] = simplified(AbstractWord.extract_metadata(head))
            if all([x in word_metadata for x in metadata_processed]):
                res_dict.append(entry)

        return res_dict

    def filter_by_complex_condition(self, complex_condition: str):
        """
        :param complex_condition: string composed of simple conditions separated by pipe ex. verb I | noun m II
        :return: subset of dict containing entries fulfilling selected criteria
        """

        simple_conditions: [str] = complex_condition.split('|')

        res_dict = Dictionary(entries=[], lang=self.lang)

        for condition in simple_conditions:
            condition_lst = [x.lower().strip() for x in condition.split(' ') if len(x) > 0]
            possible_addition = self.filter_by_simple_condition(condition_lst).entries
            for entry in possible_addition:
                if entry not in res_dict.entries:
                    res_dict.entries.append(entry)  # quadratic complexity but it's probably ok

        return res_dict

    # todo what about non existing translations/entries ?
    def remove_single_translation(self, dict_entry, translation):
        # if this is last translation remove the whole entry
        entry = [x for x in self.entries if x == dict_entry][0]
        if len(entry.translations) == 1:
            self.remove_entry(dict_entry)
        else:
            entry.translations.remove(translation)

    def length(self):
        return len(self.entries)

    def translations_nr(self) -> int:
        return len(flatten(x.translations for x in self.entries))

    def weak_index(self, base_to_be_found):
        """
        finds index of the word using weak compare
        """
        for i in range(self.length()):
            current_item = self.entries[i]
            if weak_equals(current_item.head.base, base_to_be_found):
                return i

        return None

    def find_by_header_using_weak_compare(self, to_be_found) -> list[DictionaryEntry]:
        """
        compares (weakly, that is no special signs, accents ect.) given word to any entry in dictionary part by part
        ex. in case of verb entry any of it's form (infinitive, 1p, perf, supine) will be checked (but no metadata)
        ex. "castigare" vs "castīgo, castīgāre, castīgāvī, castīgātum [verb] [I]" -> OK
        :param to_be_found:
        :return:
        """
        results: list[DictionaryEntry] = []
        for entry in self.entries:
            head_raw = entry.head.head_raw
            words_to_compare = [x for x in re.split('[, ]', head_raw) if len(x) > 0 and not x.startswith('[')]
            if any([weak_equals(x, to_be_found) for x in words_to_compare]):
                results.append(entry)

        return results

    # todo test it (1-el dict, 2-el dict)
    def random_dict_entry(self, rng=default_rng()) -> DictionaryEntry:
        random_index = rng.integers(low=0, high=self.length())
        return self.entries[random_index]  # todo rng.choice would be better ?

    # returns base and one particular translation instead of the whole dict entry
    def random_entry_with_translation(self, rng=default_rng()) -> DictEntryWithSingleTranslationHighlighted:
        # all word/translation pairs
        # get random

        dict_entries_with_single_translation = []
        for entry in self.entries:
            for translation in entry.translations:
                dict_entries_with_single_translation.append(
                    DictEntryWithSingleTranslationHighlighted(entry, translation))

        return rng.choice(dict_entries_with_single_translation)

    # todo test it ?
    def dict_words_df(self) -> pd.DataFrame:
        dict_words_placeholder = dict()

        i = 0
        for entry in self.entries:
            for translation in entry.translations:
                dict_words_placeholder[i] = [entry.head.base, translation]
                i += 1

        return pd.DataFrame.from_dict(dict_words_placeholder) \
            .transpose().rename(columns={0: 'translation', 1: 'word_pl'})

    def words_to_be_asked(self, db: pd.DataFrame, n_last_times: int) -> pd.DataFrame:
        dict_words = self.dict_words_df()

        db_merged_with_dict = db.merge(dict_words, left_on=['translation', 'word_pl'],
                                       right_on=['translation', 'word_pl'], how='right') \
            .sort_values(by='time', ascending=True, na_position='first', inplace=False)

        last_time_per_word = db_merged_with_dict.groupby(['translation', 'word_pl'])[
            'time'].last().to_frame().reset_index().rename(
            columns={'time': 'last_time'})

        df_merged_last_time = db_merged_with_dict.merge(last_time_per_word, left_on=['translation', 'word_pl'],
                                                        right_on=['translation', 'word_pl'], how='left') \
            .drop(['time', 'correct'], axis=1, inplace=False) \
            .drop_duplicates()

        last_n_times = db_merged_with_dict.groupby(['translation', 'word_pl'])[['time', 'correct']].apply(
            lambda x: x.tail(n_last_times)).reset_index().drop('level_2', axis=1)

        correct_ratio_col_name = f'correct_ratio_last_{n_last_times}_times'

        correct_ratio_last_n_times = last_n_times.groupby(['word_pl', 'translation'])[
            'correct'].mean().to_frame().reset_index() \
            .rename(columns={'correct': correct_ratio_col_name})

        df_with_statistics = db_merged_with_dict.merge(correct_ratio_last_n_times, left_on=['translation', 'word_pl'],
                                                       right_on=['translation', 'word_pl'], how='right') \
            .drop(['correct', 'time'], axis=1) \
            .drop_duplicates() \
            .merge(df_merged_last_time, left_on=['translation', 'word_pl'], right_on=['translation', 'word_pl']) \
            .sort_values('last_time', na_position='first') \
            .reset_index().drop('index', axis=1)

        df_with_statistics_last_time_null = df_with_statistics[df_with_statistics.last_time.isnull()]
        df_with_statistics_last_time_not_null = df_with_statistics[~df_with_statistics.last_time.isnull()].sort_values(
            by=[correct_ratio_col_name, 'last_time'])

        df_concatenated = pd.concat([df_with_statistics_last_time_null, df_with_statistics_last_time_not_null]) \
            .reset_index().drop('index', axis=1)

        return df_concatenated

    def word_distribution(self, df_concatenated: pd.DataFrame, n_last_times: int) -> pd.DataFrame:
        correct_ratio_col_name = f'correct_ratio_last_{n_last_times}_times'  # unfortunately it's duplicated from the method above
        rng = np.flip(self.weights_for_probabilities(len(df_concatenated)))
        s = sum(rng)
        probabilities = [x / s for x in rng]

        df_final = df_concatenated.assign(probabilities=probabilities).reset_index().drop('index', axis=1)

        # new words should have equal probability, without ranking
        probability_for_new_words = df_final[df_final.last_time.isnull()].probabilities.mean()
        df_final.loc[df_final.last_time.isnull(), 'probabilities'] = probability_for_new_words

        # use np.nan instead of usual one
        df_final.loc[df_final[correct_ratio_col_name].isnull(), correct_ratio_col_name] = np.nan

        return df_final

    def words_with_distribution(self, db: pd.DataFrame, n_last_times: int):
        words_table = self.words_to_be_asked(db, n_last_times)
        return self.word_distribution(words_table, n_last_times)

    @staticmethod
    def weights_for_probabilities(arr_length, modifier=0.5):
        nth_diff = [1 + n * modifier for n in range(arr_length)]
        return np.cumsum(nth_diff)

    def find_by_base_word_and_translation(self, base, word_pl) -> DictEntryWithSingleTranslationHighlighted:
        entries = [entry for entry in self.entries if entry.head.base == base and word_pl in entry.translations]

        if len(entries) > 1:
            raise Exception(
                f'word/translation pair should always be unique ! this is apparently not the case for {base}/{word_pl} (found {entries})')
        if len(entries) == 0:
            raise Exception(f'cannot find dict entry for {base}/{word_pl}')

        return DictEntryWithSingleTranslationHighlighted(entries[0], word_pl)

    # some statistical tests ?
    def smart_random_dict_entry_with_translation(self, db_hadler: TranslationExerciseDBHandler, user: str, n_times=5,
                                                 rng=default_rng()) -> DictEntryWithSingleTranslationHighlighted:

        translation_record = db_hadler.get().query('user == @user and lang == @self.lang').drop(['user', 'lang'],
                                                                                                axis=1)

        distribution = self.words_with_distribution(translation_record, n_times)

        # find entry by combination of word_pl and translation

        words_with_translations = list(zip(distribution.word_pl.values, distribution.translation.values))
        probabilities = distribution.probabilities.values

        if np.sum(probabilities) < 0.999999:
            raise Exception(f'''probabilities sum up to {np.sum(probabilities)} instead to 1: \n{distribution}''')

        choice = rng.choice(words_with_translations, p=probabilities)
        word_pl = choice[0]
        word_original = choice[1]

        return self.find_by_base_word_and_translation(base=word_original, word_pl=word_pl)
