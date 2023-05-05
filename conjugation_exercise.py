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

    user_input = 'y'
    while user_input.lower() != 'n' and len(conjugations_filtered.records) > 0:
        conjugation_record = conjugations_filtered.random_record(rng)
        print(conjugation_record.infinitive, conjugation_record.mood.value.lower(),
              conjugation_record.tense.value.lower(), conjugation_record.voice.value.lower(),
              conjugation_record.person.value, 'person', conjugation_record.number.value.lower())
        user_answer = input()
        if weak_equals(user_answer, conjugation_record.word):
            print('correct', end='\n\n')
            if args.remove is not None:
                conjugations_filtered.records.remove(conjugation_record)
                if len(conjugations_filtered.records) % 10 == 0:
                    print(f'{len(conjugations_filtered.records)} left')
        else:
            print(f'wrong. proper answer is {conjugation_record.word}', end='\n\n')

    print('terminating..')
