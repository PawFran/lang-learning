import os

import pytest

from lib.parsing_dict import *

test_files_dir = 'test'
test_files_name = 'latin_test.txt'
dict_path = os.path.join(test_files_dir, test_files_name)

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


def test_read_file_raw():
    assert read_file_raw(dict_path) == lines_raw


@pytest.mark.parametrize('lines', [lines_raw, lines_raw_blank_line_at_the_end])
def test_group_raw_lines(lines):
    assert group_raw_lines(lines) == lines_grouped


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
