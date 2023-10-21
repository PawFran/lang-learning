import os

from common.lib.utils import weak_equals
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args
from conjugation.lib.utils import filter_conjugations

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("conjugation", "resources", "conjugation.json")

    args = parse_args()

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)
    conjugations_filtered: ConjugationTable = filter_conjugations(conjugation_all_table, args)

    print(f'{len(conjugations_filtered.records)} left')

    print()

    should_continue = True
    while should_continue and len(conjugations_filtered.records) > 0:
        verb = conjugations_filtered.random_record(rng)
        print(verb.summary())

        try:
            user_answer = input()
            if weak_equals(user_answer, verb.word):
                print('correct', end='\n\n')
                if not args.keep:
                    conjugations_filtered.records.remove(verb)
                    if len(conjugations_filtered.records) % 10 == 0:
                        print(f'{len(conjugations_filtered.records)} left\n')
            else:
                print(f'wrong. proper answer is {verb.word}', end='\n\n')
        except KeyboardInterrupt:
            should_continue = False
            print('')

    print('terminating..')
