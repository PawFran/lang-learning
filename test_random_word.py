import pytest
from random_word import *

dict_path = 'latin_test.txt'
lines_raw = \
    ['castīgo, āre, avi, atum [verb] [I]\n',
     '(Ancillam miseram domina sevēra castīgat)\n',
     '1. karać\n',
     '\n',
     'multae, ārum [noun] [I] [pl]\n',
     '(Multae viae Varsoviae longae et latae sunt)\n',
     '1. liczne\n',
     '\n',
     'valdē [adv]\n',
     '(Varsoviam valde amamus)\n',
     '1. bardzo']
lines_raw_blank_line_at_the_end = lines_raw + ['\n']
lines_grouped = \
    [
        ['castīgo, āre, avi, atum [verb] [I]\n',
         '(Ancillam miseram domina sevēra castīgat)\n',
         '1. karać\n'],
        ['multae, ārum [noun] [I] [pl]\n',
         '(Multae viae Varsoviae longae et latae sunt)\n',
         '1. liczne\n'],
        ['valdē [adv]\n',
         '(Varsoviam valde amamus)\n',
         '1. bardzo']
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
    assert conjugation(head_first_conj) == 'I'
    assert conjugation(head_second_conj) == 'II'
    assert conjugation(head_third_conj) == 'III'
    # add IIIa ?
    assert conjugation(head_fourth_conj) == 'IV'


def test_declension():
    assert declension(head_first_declension) == 'I'
    assert declension(head_second_declension) == 'II'
    assert declension(head_third_vowel_declension) == 'III vowel'
    assert declension(head_third_consonant_declension) == 'III consonant'
    assert declension(head_third_mixed_declension) == 'III mixed'
    assert declension(head_fourth_declension) == 'IV'
    assert declension(head_fifth_declension) == 'V'


def test_only_plural():
    assert only_plural('multae, ārum [noun] [I] [pl]')
    assert not only_plural('vinea, ae [noun] [I] [f]')


#@pytest.mark.skip(reason="not ready")
def test_parse_entry():
    assert parse_dict_entry(lines_grouped[0]) is not None
