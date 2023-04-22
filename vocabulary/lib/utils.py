import re

from numpy.random import default_rng


# todo test it
def extract_from_square_brackets(pattern, line):
    match = re.search(pattern, line)
    if match is not None:
        return match.group().replace('[', '').replace(']',
                                                      '')  # should be possible by using some groups in re directly ?
    else:
        return None


# todo move it to dict class ?
def random_dict_entry(dictionary, rng=default_rng()):
    random_index = rng.integers(low=0, high=dictionary.length())
    return dictionary.entries[random_index]
