import re
from common.lib.utils import weak_equals
from vocabulary.lib.dict_classes import LatinVerb, LatinAdjective


def compare_answer_with_full_head_raw(head_raw, to_compare) -> bool:
    """
    apart from normal weak comparison a few shortcuts are possible
    after first conjugation verb typing ending 'āre, āvi, ātum' is ok
    after adjective with three endings typing ending 'a, um' is ok
    """

    def to_list_no_metadata(s):
        return [x for x in re.split('[ ,]', s) if len(x) > 0 and not x.startswith('[')]

    def all_elements_equal(l1, l2) -> bool:
        return all([weak_equals(x, y) for (x, y) in zip(l1, l2)])

    def all_elements_equal_verb_shortcut(original, to_compare) -> bool:
        shortcut_pattern = ['āre', 'āvi', 'ātum']
        if len(original) != len(to_compare):
            return False
        else:
            return weak_equals(original[0], to_compare[0]) and all_elements_equal(shortcut_pattern, to_compare[1:])

    # TODO use it. use method for both adj and verb
    def all_elements_equal_adjective_shortcut(original, to_compare) -> bool:
        shortcut_pattern = ['a', 'um']
        if len(original) != len(to_compare):
            return False
        else:
            return weak_equals(original[0], to_compare[0]) and all_elements_equal(shortcut_pattern, to_compare[1:])

    head_to_list_no_metadata = to_list_no_metadata(head_raw)
    to_compare_list = to_list_no_metadata(to_compare)

    if len(head_to_list_no_metadata) == len(to_compare_list):
        if LatinVerb.is_verb(head_raw):
            if LatinVerb.which_conjugation(head_raw) == 'I':
                return (all_elements_equal(head_to_list_no_metadata, to_compare_list) or
                        all_elements_equal_verb_shortcut(head_to_list_no_metadata, to_compare_list))
        # elif LatinAdjective.is_adjective(head_raw):
        else:
            return all_elements_equal(head_to_list_no_metadata, to_compare_list)
    else:
        return False
