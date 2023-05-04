import os

from common.lib.utils import weak_equals
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args
from conjugation.lib.utils import filter_conjugations

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("conjugation", "resources", "conjugation.json")

    args = parse_args()

    print(f'remove? {args.remove} (not implemented)')

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)
    conjugations_filtered: ConjugationTable = filter_conjugations(conjugation_all_table, args)

    print()

    user_input = 'y'
    while user_input.lower() != 'n':
        conjugation_record = conjugations_filtered.random_record(rng)
        print(conjugation_record.infinitive, conjugation_record.mood.name.lower(),
              conjugation_record.tense.name.lower(), conjugation_record.voice.name.lower(),
              conjugation_record.person.value, 'person', conjugation_record.number.name.lower())
        user_answer = input()
        if weak_equals(user_answer, conjugation_record.word):
            print('correct', end='\n\n')
        else:
            print(f'wrong. proper answer is {conjugation_record.word}', end='\n\n')
