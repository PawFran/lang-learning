import re
from common.lib.utils import weak_equals
from vocabulary.lib.dict_classes import LatinVerb, LatinAdjective


def compare_answer_with_full_head_raw(entry_head, answer) -> bool:
    """
    apart from normal weak comparison a few shortcuts are possible
    after first conjugation verb both are ok:
        * typing ending 'āre, āvi, ātum'
        * typing '1'
    after adjective with three endings typing ending 'a, um' is ok
    """

    def to_list_no_metadata(s):
        return [x for x in re.split('[ ,]', s) if len(x) > 0 and not x.startswith('[')]

    def all_elements_equal(l1, l2) -> bool:
        return all([weak_equals(x, y) for (x, y) in zip(l1, l2)])

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

    # TODO use it
    def all_elements_equal_adjective_shortcut(original, to_compare) -> bool:
        adj_pattern = ['a', 'um']
        return all_elements_equal_ending_shortcut(original, to_compare, adj_pattern)

    original_as_list = to_list_no_metadata(entry_head)
    answer_as_list = to_list_no_metadata(answer)

    if LatinVerb.is_verb(entry_head):
        if LatinVerb.which_conjugation(entry_head) == 'I':
            return (all_elements_equal(original_as_list, answer_as_list) or
                    all_elements_equal_verb_ending_shortcut(original_as_list, answer_as_list) or
                    all_elements_equal_verb_number_shortcut(original_as_list, answer_as_list))
        else:
            return all_elements_equal(original_as_list, answer_as_list)
    # elif LatinAdjective.is_adjective(head_raw):
    else:
        return all_elements_equal(original_as_list, answer_as_list)
