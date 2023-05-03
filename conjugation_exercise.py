import os

from numpy.random import default_rng

from common.lib.utils import weak_equals
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("conjugation", "resources", "conjugation.json")

    args = parse_args()

    print(f'conjugations to filter: {args.conjugations}')
    print(f'remove? {args.remove} (not implemented)')

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)

    conjugations_to_include = [*ConjugationType] if args.conjugations is None else [ConjugationType.from_string(s)
                                                                                    for s in args.conjugations]
    moods_to_include = [*Mood] if args.moods is None else [Mood.from_string(s) for s in args.moods]
    tenses_to_include = [*Tense] if args.tenses is None else [Tense.from_string(s) for s in args.tenses]
    voices_to_include = [*Voice] if args.voices is None else [Voice.from_string(s) for s in args.voices]

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
        print(conjugation_record.infinitive, conjugation_record.mood.name.lower(),
              conjugation_record.tense.name.lower(), conjugation_record.voice.name.lower(),
              conjugation_record.person.value, 'person', conjugation_record.number.name.lower())
        user_answer = input()
        if weak_equals(user_answer, conjugation_record.word):
            print('correct', end='\n\n')
        else:
            print(f'wrong. proper answer is {conjugation_record.word}', end='\n\n')
