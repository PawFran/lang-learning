import re
from numpy.random import default_rng
from argparse import ArgumentParser
import os


def extract_from_square_brackets(pattern, line):
    match = re.search(pattern, line)
    if match is not None:
        return match.group().replace('[', '').replace(']',
                                                      '')  # should be possible by using some groups in re directly ?
    else:
        return None


def random_dict_entry(dictionary, rng=default_rng()):
    random_index = rng.integers(low=0, high=len(dictionary.entries))
    return dictionary.entries[random_index]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-l', '--language', action='store')
    parser.add_argument('-r', '--remove', action='store_true')
    return parser.parse_args()


def parse_dict_path(language, dicts_folder):
    dict_file_name = f'{language}.txt'
    return os.path.join(dicts_folder, dict_file_name)
