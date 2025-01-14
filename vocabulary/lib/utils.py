import os
import re

from common.lib.utils import weak_equals, replace_special
from vocabulary.lib.dict_classes import LatinVerb, LatinAdjective

DICT_DIR_PATH = os.path.join('vocabulary', 'dicts')


# TODO test
def to_list_no_metadata(s):
    return [x for x in re.split('[ ,]', s) if len(x) > 0 and not x.startswith('[')]


# TODO test
def all_elements_equal(l1, l2) -> bool:
    if len(l1) != len(l2):
        return False
    else:
        return all([weak_equals(x, y) for (x, y) in zip(l1, l2)])


# TODO move it to LatinAdjective class ? use sth like AdjectiveType in the future
def adjective_first_and_second_declension(adj):
    adj_as_list = to_list_no_metadata(adj)
    return weak_equals(adj_as_list[1][-1], 'a') and weak_equals(adj_as_list[2][-2:], 'um')


def compose_with_or(*functions):
    def composed_function(*args, **kwargs):
        return any(f(*args, **kwargs) for f in functions)

    return composed_function


def equality_ending_shortcut(original, to_compare, shortcut_pattern) -> bool:
    return len(original) == len(to_compare) and \
           weak_equals(original[0], to_compare[0]) and \
           all_elements_equal(shortcut_pattern, to_compare[1:])


def equality_number_shortcut(original, to_compare, shortcut_number) -> bool:
    if len(to_compare) != 2:
        return False
    else:
        return weak_equals(original[0], to_compare[0]) and all_elements_equal(shortcut_number, to_compare[1])


def equality_verb_ending_shortcut(original, to_compare) -> bool:
    shortcut_pattern = ['āre', 'āvi', 'ātum']
    return equality_ending_shortcut(original, to_compare, shortcut_pattern)


# TODO for later
# def equality_noun_ending_shortcut(original, to_compare) -> bool:
#     shortcut_pattern = ['ae']
#     return equality_ending_shortcut(original, to_compare, shortcut_pattern)


# ex. 'castigo castigare castigavi castigatum' == 'castigo 1'
def equality_verb_number_shortcut(original, to_compare) -> bool:
    shortcut_number = '1'
    return equality_number_shortcut(original, to_compare, shortcut_number)


# ex. 'ferus fera ferum' == 'ferus a um'
def equality_adjective_ending_shortcut(original, to_compare) -> bool:
    adj_pattern = ['a', 'um']
    return equality_ending_shortcut(original, to_compare, adj_pattern)


# ex. 'ferox ferox ferox' == 'ferox x3'
def equality_adjective_number_shortcut(correct_forms: list[str], answer: list[str]) -> bool:
    return all_forms_are_the_same(correct_forms) and \
           answer[0] == correct_forms[0] and \
           answer[1].lower().strip() == 'x3'

verb_shortcuts = compose_with_or(all_elements_equal, equality_verb_ending_shortcut,
                                 equality_verb_number_shortcut)

adjective_ending_shortcuts = compose_with_or(all_elements_equal, equality_adjective_ending_shortcut)

adjective_number_shortcuts = compose_with_or(all_elements_equal, equality_adjective_number_shortcut)


def all_forms_are_the_same(forms: list[str]) -> bool:
    return len(set(forms)) == 1


def ending_are_avi_atum(forms: list[str]) -> bool:
    if len(forms) != 4:
        return False

    forms_simplified = [replace_special(s).strip() for s in forms]

    return forms_simplified[1].endswith('are') and \
        forms_simplified[2].endswith('avi') and \
        forms_simplified[3].endswith('atum')


def compare_answer_with_full_head_raw(entry_head, answer) -> bool:
    """
    apart from normal weak comparison a few shortcuts are possible
    after first conjugation verb both are ok:
        * typing ending 'āre, āvi, ātum'
        * typing '1'
    after adjective of 1/2 declension 'a, um' is ok
    after adjective with three identical forms typing 'x3' is ok
    """

    original_as_list = to_list_no_metadata(entry_head)
    answer_as_list = to_list_no_metadata(answer)

    if LatinVerb.is_verb(entry_head) and ending_are_avi_atum(original_as_list):
        return verb_shortcuts(original_as_list, answer_as_list)
    elif LatinAdjective.is_adjective(entry_head) and len(answer_as_list) == 3 and adjective_first_and_second_declension(
            entry_head):
        return adjective_ending_shortcuts(original_as_list, answer_as_list)
    elif LatinAdjective.is_adjective(entry_head) and all_forms_are_the_same(original_as_list):
        return adjective_number_shortcuts(original_as_list, answer_as_list)
    else:
        return all_elements_equal(original_as_list, answer_as_list)
