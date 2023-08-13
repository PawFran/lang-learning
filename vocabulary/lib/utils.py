import re
from common.lib.utils import weak_equals


# todo test it
def extract_from_square_brackets(pattern, line):
    match = re.search(pattern, line)
    if match is not None:
        return match.group().replace('[', '').replace(']',
                                                      '')  # should be possible by using some groups in re directly ?
    else:
        return None


def compare_answer_with_full_head_raw(head_raw, to_compare) -> bool:
    def to_list_no_metadata(s):
        return [x for x in re.split('[ ,]', s) if len(x) > 0 and not x.startswith('[')]

    def compare_by_element(l1, l2):
        return all([weak_equals(x, y) for (x, y) in zip(l1, l2)])

    head_to_list_no_metadata = to_list_no_metadata(head_raw)
    to_compare_to_list = to_list_no_metadata(to_compare)

    if len(head_to_list_no_metadata) == len(to_compare_to_list):
        return compare_by_element(head_to_list_no_metadata, to_compare_to_list)
    else:
        return False
