import re
import os
from common.lib.utils import weak_equals
from vocabulary.lib.dict_classes import LatinVerb, LatinAdjective
from conjugation.lib.conjugation_classes import ConjugationType

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


def compare_answer_with_full_head_raw(entry_head, answer) -> bool:
    """
    apart from normal weak comparison a few shortcuts are possible
    after first conjugation verb both are ok:
        * typing ending 'āre, āvi, ātum'
        * typing '1'
    after adjective of 1/2 declension 'a, um' is ok
    after adjective with three endings typing ending '3' is ok
    """

    def all_elements_equal_ending_shortcut(original, to_compare, shortcut_pattern) -> bool:
        if len(original) != len(to_compare):
            return False
        else:
            return weak_equals(original[0], to_compare[0]) and all_elements_equal(shortcut_pattern, to_compare[1:])

    def all_elements_equal_number_shortcut(original, to_compare, shortcut_number) -> bool:
        if len(to_compare) != 2:
            return False
        else:
            return weak_equals(original[0], to_compare[0]) and all_elements_equal(shortcut_number, to_compare[1])

    def all_elements_equal_verb_ending_shortcut(original, to_compare) -> bool:
        shortcut_pattern = ['āre', 'āvi', 'ātum']
        return all_elements_equal_ending_shortcut(original, to_compare, shortcut_pattern)

    def all_elements_equal_verb_number_shortcut(original, to_compare) -> bool:
        shortcut_number = '1'
        return all_elements_equal_number_shortcut(original, to_compare, shortcut_number)

    def all_elements_equal_adjective_ending_shortcut(original, to_compare) -> bool:
        adj_pattern = ['a', 'um']
        return all_elements_equal_ending_shortcut(original, to_compare, adj_pattern)

    def all_elements_equal_adjective_number_shortcut(original, to_compare) -> bool:
        shortcut_number = '3'
        return all_elements_equal_number_shortcut(original, to_compare, shortcut_number)

    original_as_list = to_list_no_metadata(entry_head)
    answer_as_list = to_list_no_metadata(answer)

    if LatinVerb.is_verb(entry_head):
        if LatinVerb.which_conjugation(entry_head) is ConjugationType.I:
            return (all_elements_equal(original_as_list, answer_as_list) or
                    all_elements_equal_verb_ending_shortcut(original_as_list, answer_as_list) or
                    all_elements_equal_verb_number_shortcut(original_as_list, answer_as_list))
        else:
            return all_elements_equal(original_as_list, answer_as_list)
    elif LatinAdjective.is_adjective(entry_head) and len(answer_as_list) == 3:
        if adjective_first_and_second_declension(entry_head):
            return (all_elements_equal(original_as_list, answer_as_list) or
                    all_elements_equal_adjective_ending_shortcut(original_as_list, answer_as_list))
        else:
            return all_elements_equal(original_as_list, answer_as_list)
    elif LatinAdjective.is_adjective(entry_head):
        if len(set(original_as_list)) == 1:  # that is all entries are the same
            return (all_elements_equal(original_as_list, answer_as_list) or
                    all_elements_equal_adjective_number_shortcut(original_as_list, answer_as_list))
        else:
            return all_elements_equal(original_as_list, answer_as_list)
    else:
        return all_elements_equal(original_as_list, answer_as_list)
