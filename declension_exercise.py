# when third declension is mentioned all variants should be included
# todo filter by word

import os
import copy

from numpy.random import default_rng

from common.lib.utils import weak_equals
from declension.lib.parsing_args import *
from declension.lib.utils import *

if __name__ == '__main__':
    rng = default_rng()
    dict_file_path = os.path.join("declension", "resources", "declension.json")

    args = parse_args()
    print(f'declensions to filter: {args.declensions}')
    print(f'remove? {args.remove} (not implemented)')

    declension_all = Declensions.from_file_path(dict_file_path)

    declensions_to_include = [*DeclensionType]
    if args.declensions is not None:
        declensions_to_include = [DeclensionType.from_string(s) for s in args.declensions]

    print()

    declensions_filtered: Declensions = filter_by_type(declension_all, declensions_to_include)

    # todo when last entry removed summarize nr of correct/wrong answers

    current_dict = declensions_filtered

    should_continue = 'y'
    while should_continue.lower() != 'n':
        backup_dict = copy.deepcopy(current_dict)  # in case remove is on and answer is wrong
        declension_test: DeclensionTest = random_declension_entry(current_dict, rng, args.remove)
        if declension_test is None:
            should_continue = 'n'  # means all entries where already removed
        else:
            declension_prompt: DeclensionPrompt = declension_test.prompt
            print(declension_prompt.base_word, declension_prompt.case, declension_prompt.number)

            user_answer = input()
            if weak_equals(user_answer, declension_test.answer):
                print('correct', end='\n\n')
            else:
                print(f'wrong. proper answer is {declension_test.answer}', end='\n\n')
                current_dict = backup_dict

    print('terminating..')
