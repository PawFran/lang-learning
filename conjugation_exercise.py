import os

from numpy.random import default_rng

from common.lib.utils import weak_equals
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("conjugation", "resources", "conjugation.json")

    args = parse_args()  # todo add filtering by tenses, moods etc.

    print(f'conjugations to filter: {args.conjugations}')
    print(f'remove? {args.remove} (not implemented)')

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)

    conjugations_to_include = [*ConjugationType]
    if args.conjugations is not None:
        conjugations_to_include = [ConjugationType.from_string(s) for s in args.conjugations]

    print()

    conjugations_filtered: ConjugationTable = ConjugationTable([record for record in conjugation_all_table.records if
                                                                record.conjugation_type in conjugations_to_include])


    def random_conjugation_record(conjugations_table: ConjugationTable, rng=default_rng()) -> SingleConjugationRecord:
        if len(conjugations_table.records) == 0:
            raise Exception("cannot select random entry from empty dict")

        return rng.choice(conjugations_table.records)


    user_input = 'y'
    while user_input.lower() != 'n':
        conjugation_record = random_conjugation_record(conjugations_filtered, rng)
        # todo more readable prints
        print(conjugation_record.infinitive, conjugation_record.mood, conjugation_record.tense,
              conjugation_record.voice, conjugation_record.number, conjugation_record.person)
        user_answer = input()
        if weak_equals(user_answer, conjugation_record.word):
            print('correct', end='\n\n')
        else:
            print(f'wrong. proper answer is {conjugation_record.word}', end='\n\n')
