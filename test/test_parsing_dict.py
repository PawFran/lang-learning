import os

import pytest

from lib.parsing_dict import *

test_files_dir = os.path.join('test', 'resources')
test_files_name = 'latin_test.txt'
dict_path = os.path.join(test_files_dir, test_files_name)

lines_raw_latin = \
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
lines_raw_latin_blank_line_at_the_end = lines_raw_latin + ['\n']
lines_grouped_latin = \
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

lines_raw_english = \
    ['impel [verb]\n',
     '(I never read medicine advertisement without being impelled to the conclusion that I am suffering from the particular disease)\n',
     '1. to make someone feel that they must do something\n',
     '2. to force someone to do something\n']


def test_read_file_raw():
    assert read_file_raw(dict_path) == lines_raw_latin


@pytest.mark.parametrize('lines', [lines_raw_latin, lines_raw_latin_blank_line_at_the_end])
def test_group_raw_lines(lines):
    assert group_raw_lines(lines) == lines_grouped_latin


def test_parse_example():
    assert parse_example('(Marīa amīcam amat et laudat)') == 'Marīa amīcam amat et laudat'
    assert parse_example('(Marīa amīcam amat et laudat)\n') == 'Marīa amīcam amat et laudat'
    assert parse_example('Marīa amīcam amat et laudat') == 'Marīa amīcam amat et laudat'
    assert parse_example('Marīa amīcam amat (et laudat)') == 'Marīa amīcam amat (et laudat)'


def test_parse_translation():
    assert parse_translation('1. winnica') == 'winnica'


def test_parse_single_group_of_lines():
    parsed = parse_single_group_of_lines(lines_grouped_latin[0])
    assert parsed[0] == 'castīgo, āre, avi, atum [verb] [I]'
    assert parsed[1] == 'Ancillam miseram domina sevēra castīgat'
    assert parsed[2] == ['karać']


def test_parse_latin_entry():
    dict_entry = parse_latin_dict_entry(
        ['castīgo, āre, avi, atum [verb] [I]\n',
         '(Ancillam miseram domina sevēra castīgat)\n',
         '1. karać\n']
    )

    assert dict_entry.head == LatinVerb(
        base='castīgo',
        head_raw='castīgo, āre, avi, atum [verb] [I]',
        infinite='āre',
        perfect='avi',
        supine='atum',
        conjugation='I'
    )

    assert dict_entry.example == 'Ancillam miseram domina sevēra castīgat'
    assert dict_entry.translations == ['karać']


def test_parse_english_entry():
    dict_entry = parse_english_dict_entry(
        ['impel [verb]',
         '(I never read medicine advertisement without being impelled to the conclusion that I am suffering from the particular disease)\n',
         '1. to make someone feel that they must do something\n',
         '2. to force someone to do something\n']
    )

    assert dict_entry.head == EnglishWord(
        base='impel',
        head_raw='impel [verb]',
        part_of_speech='verb'
    )

    assert dict_entry.example == 'I never read medicine advertisement without being impelled to the conclusion that I am suffering from the particular disease'
    assert dict_entry.translations == ['to make someone feel that they must do something',
                                       'to force someone to do something']


def test_parse_latin_dict():
    dictionary = parse_latin_dict(lines_raw_latin)
    assert dictionary.entries[0] == DictionaryEntry(
        head=LatinVerb(
            base='castīgo',
            head_raw='castīgo, āre, avi, atum [verb] [I]',
            infinite='āre',
            perfect='avi',
            supine='atum',
            conjugation='I'
        ),
        example='Ancillam miseram domina sevēra castīgat',
        translations=['karać']
    )


def test_parse_english_dict():
    dictionary = parse_english_dict(lines_raw_english)
    assert dictionary.entries[0] == DictionaryEntry(
        head=EnglishWord(
            base='impel',
            head_raw='impel [verb]',
            part_of_speech='verb'
        ),
        example='I never read medicine advertisement without being impelled to the conclusion that I am suffering from the particular disease',
        translations=['to make someone feel that they must do something', 'to force someone to do something']
    )


def test_parse_dict_subset():
    dict_entry1 = DictionaryEntry(
        head=LatinAdverb(base='saepe', head_raw='saepe [adv]'),
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )

    dict_entry2 = DictionaryEntry(
        head=LatinAdverb(base='valdē', head_raw='valdē [adv]'),
        example='Varsoviam valde amamus',
        translations=['bardzo']
    )
    dict_entry3 = DictionaryEntry(
        head=LatinAdjective(
            base='sempiternus', head_raw='sempiternus, a, um [adj]',
            femininum='a', neutrum='um'),
        example='Verae amicitiae sempiternae sunt',
        translations=['ciągły, trwały, wieczny']
    )

    dictionary = Dictionary([dict_entry1, dict_entry2, dict_entry3])

    assert dict_subset(dictionary).length() == 3

    assert dict_subset(dictionary, start_word='saepe').length() == 3
    assert dict_subset(dictionary, start_word='valdē').length() == 2
    assert dict_subset(dictionary, start_word='valde').length() == 2
    assert dict_subset(dictionary, start_word='sempiternus').length() == 1

    assert dict_subset(dictionary, start_word='laudo') is None
    assert dict_subset(dictionary, end_word='laudo') is None

    # start after end
    assert dict_subset(dictionary, start_word='sempiternus', end_word='valde') is None

    assert dict_subset(dictionary, start_word='saepe', end_word='valde').length() == 2
    assert dict_subset(dictionary, start_word='saepe', end_word='saepe').length() == 1

    assert dict_subset(dictionary, end_word='valde').length() == 2

