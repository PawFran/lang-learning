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
    args = parse_args()

    dict_file_path = os.path.join("declension", "resources", "declension.json")

    declension_all = Declensions.from_file_path(dict_file_path)

    declensions_to_include = [*DeclensionType]
    if args.declensions is not None:
        print(f'declensions to filter: {args.declensions}')
        declensions_to_include = [DeclensionType.from_string(s) for s in args.declensions]

    print()

    declensions_filtered: Declensions = filter_by_type(declension_all, declensions_to_include)

    print(f'current nr of entries: {declensions_filtered.length()}')

    # todo when last entry removed summarize nr of correct/wrong answers

    current_dict = declensions_filtered

    should_continue = True
    while should_continue:
        backup_dict = copy.deepcopy(current_dict)  # in case remove is on and answer is wrong
        pop = False if args.keep else True
        declension_test: DeclensionTest = random_declension_entry(current_dict, rng,
                                                                  pop)  # here current_dict may be modified
        if declension_test is None:
            should_continue = False  # means all entries where already removed
        else:
            declension_prompt: DeclensionPrompt = declension_test.prompt
            print(declension_prompt.base_word, declension_prompt.case, declension_prompt.number)

            try:
                user_answer = input()
                if weak_equals(user_answer, declension_test.answer):
                    print('correct', end='\n\n')
                else:
                    print(f'wrong. proper answer is {declension_test.answer}', end='\n\n')
                    current_dict = backup_dict
            except KeyboardInterrupt:
                should_continue = False
                print('')

        if not args.keep:
            current_length = current_dict.length()
            if current_length % 10 == 0:
                print(f'current nr of entries: {current_length}')

    print('terminating..')
