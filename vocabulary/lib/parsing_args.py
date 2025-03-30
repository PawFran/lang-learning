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
    parser.add_argument('-r', '--revise_last_session', action='store_true') # take only words from last session which were not answered correctly at first time
    parser.add_argument('-n', '--number_of_synonyms', action='store')
    return parser.parse_args()


def parse_dict_path(language, dicts_folder):
    dict_file_name = f'{language}.txt'
    return os.path.join(dicts_folder, dict_file_name)
