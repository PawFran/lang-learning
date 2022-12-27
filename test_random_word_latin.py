import pytest
from parsing_dict import *

dict_path = 'latin_test.txt'
lines_raw = \
    ['castīgo, āre, avi, atum [verb] [I]\n',
     '(Ancillam miseram domina sevēra castīgat)\n',
     '1. karać\n',
     '\n',
     'vinea, ae [noun] [I] [f]\n',
     '(Ancillae in vineā labōrant)\n',
     '1. winnica\n',
     '\n',
     'valdē [adv]\n',
     '(Varsoviam valde amamus)\n',
     '1. bardzo\n',
     '\n',
     'sempiternus, a, um [adj]\n',
     '(Verae amicitiae sempiternae sunt)\n',
     '1. ciągły, trwały, wieczny']
lines_raw_blank_line_at_the_end = lines_raw + ['\n']
lines_grouped = \
    [
        ['castīgo, āre, avi, atum [verb] [I]\n',
         '(Ancillam miseram domina sevēra castīgat)\n',
         '1. karać\n'],
        ['vinea, ae [noun] [I] [f]\n',
         '(Ancillae in vineā labōrant)\n',
         '1. winnica\n'],
        ['valdē [adv]\n',
         '(Varsoviam valde amamus)\n',
         '1. bardzo\n'],
        ['sempiternus, a, um [adj]\n',
         '(Verae amicitiae sempiternae sunt)\n',
         '1. ciągły, trwały, wieczny']
    ]

head_first_conj = 'castīgo, āre, avi, atum [verb] [I]'
head_second_conj = 'maneō, ēre, sī, sum [verb] [II]'
head_third_conj = 'ostendō, ere, dī, tum(sum) [verb] [III]'
head_fourth_conj = 'sentiō, īre, sī, sum [verb] [IV]'

head_first_declension = 'cōpia, ae [noun] [I] [f]'
head_second_declension = 'exiguum, ī [noun] [II] [n]'
head_third_vowel_declension = 'omnia, ium [noun] [III vowel] [n] [pl]'
head_third_consonant_declension = 'hospes, itis [noun] [III consonant] [m]'
head_third_mixed_declension = 'turris, is [noun] [III mixed] [f]'
head_fourth_declension = 'equitātus, ūs [noun] [IV] [m]'
head_fifth_declension = 'saniēs, ēī [noun] [V] [f]'


def test_read_file_raw():
    assert read_file_raw(dict_path) == lines_raw


@pytest.mark.parametrize('lines', [lines_raw, lines_raw_blank_line_at_the_end])
def test_group_raw_lines(lines):
    assert group_raw_lines(lines) == lines_grouped


def test_conjugation():
    assert Verb.which_conjugation(head_first_conj) == 'I'
    assert Verb.which_conjugation(head_second_conj) == 'II'
    assert Verb.which_conjugation(head_third_conj) == 'III'
    # add IIIa ?
    assert Verb.which_conjugation(head_fourth_conj) == 'IV'


def test_declension():
    assert Noun.which_declension(head_first_declension) == 'I'
    assert Noun.which_declension(head_second_declension) == 'II'
    assert Noun.which_declension(head_third_vowel_declension) == 'III vowel'
    assert Noun.which_declension(head_third_consonant_declension) == 'III consonant'
    assert Noun.which_declension(head_third_mixed_declension) == 'III mixed'
    assert Noun.which_declension(head_fourth_declension) == 'IV'
    assert Noun.which_declension(head_fifth_declension) == 'V'


def test_is_verb():
    assert Verb.is_verb('castīgo, āre, avi, atum [verb] [I]')
    assert not Verb.is_verb('vinea, ae [noun] [I] [f]')


def test_verb_from_entry_head():
    line = 'castīgo, āre, avi, atum [verb] [I]'
    verb = Verb.from_entry_head(line)
    assert verb.base == 'castīgo'
    assert verb.infinite == 'āre'
    assert verb.perfect == 'avi'
    assert verb.supine == 'atum'
    assert verb.conjugation == 'I'
    # todo handle and test case when not all forms are given


def test_is_noun():
    assert not Noun.is_noun('castīgo, āre, avi, atum [verb] [I]')
    assert Noun.is_noun('vinea, ae [noun] [I] [f]')


def test_which_genre():
    assert Noun.which_genre('vinea, ae [noun] [I] [f]') == 'f'
    # todo add other examples


def test_only_plural():
    assert Noun.is_only_plural('multae, ārum [noun] [I] [pl]')
    assert not Noun.is_only_plural('vinea, ae [noun] [I] [f]')


def test_noun_from_entry_head():
    line = 'vinea, ae [noun] [I] [f]'
    noun = Noun.from_entry_head(line)
    assert noun.base == 'vinea'
    assert noun.genetive == 'ae'
    assert noun.genre == 'f'
    assert not noun.only_plural
    assert noun.declension == 'I'
    # todo add onl plural noun


def test_is_adverb():
    assert Adverb.is_adverb('saepe [adv]')
    assert not Adverb.is_adverb('vinea, ae [noun] [I] [f]')


def test_adverb_from_entry_head():
    adverb = Adverb.from_entry_head('saepe [adv]')
    assert adverb.base == 'saepe'


def test_is_adjective():
    assert Adjective.is_adjective('sempiternus, a, um [adj]')
    assert not Adjective.is_adjective('saepe [adv]')


def test_adjective_from_entry_head():
    adjective = Adjective.from_entry_head('sempiternus, a, um [adj]')
    assert adjective.base == 'sempiternus'
    assert adjective.femininum == 'a'
    assert adjective.neutrum == 'um'


# TODO test all methods from subtypes of AbstractWord: Verb, Noun etc.
# todo split tets into different files ex. separate tests for verb methods etc.

def test_parse_example():
    assert parse_example('(Marīa amīcam amat et laudat)') == 'Marīa amīcam amat et laudat'
    assert parse_example('(Marīa amīcam amat et laudat)\n') == 'Marīa amīcam amat et laudat'
    assert parse_example('Marīa amīcam amat et laudat') == 'Marīa amīcam amat et laudat'
    assert parse_example('Marīa amīcam amat (et laudat)') == 'Marīa amīcam amat (et laudat)'


def test_parse_translation():
    assert parse_translation('1. winnica') == 'winnica'


@pytest.mark.skip(reason='not ready')
def test_parse_entry():
    assert parse_dict_entry(lines_grouped[0]) is not None
