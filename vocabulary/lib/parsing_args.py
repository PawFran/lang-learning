import os
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-l', '--language', action='store')
    parser.add_argument('-k', '--keep', action='store_true')
    parser.add_argument('-a', '--start_word', action='store')  # todo does it work with smart sampling ?
    parser.add_argument('-z', '--end_word', action='store')  # todo does it work with smart sampling ?
    parser.add_argument('-u', '--user_name', action='store')
    parser.add_argument('-t', '--top', action='store')
    parser.add_argument('-f', '--filter', action='store')
    return parser.parse_args()


def parse_dict_path(language, dicts_folder):
    dict_file_name = f'{language}.txt'
    return os.path.join(dicts_folder, dict_file_name)
