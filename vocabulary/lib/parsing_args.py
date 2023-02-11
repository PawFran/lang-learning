import os
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-l', '--language', action='store')
    parser.add_argument('-r', '--remove', action='store_true')
    parser.add_argument('-a', '--start_word', action='store')
    parser.add_argument('-z', '--end_word', action='store')
    return parser.parse_args()


def parse_dict_path(language, dicts_folder):
    dict_file_name = f'{language}.txt'
    return os.path.join(dicts_folder, dict_file_name)
