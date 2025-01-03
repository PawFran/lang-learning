import os

from actions.conjugation import CONJUGATION_EXERCISE_CSV_LOG_FILE_PATH
from common.lib.utils import weak_equals, DEFAULT_USER_NAME
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args
from conjugation.lib.utils import filter_conjugations
from vocabulary.lib.file_db import ConjugationExerciseCSVHandler

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("conjugation", "resources", "conjugation.json")

    args = parse_args()

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)
    conjugations_filtered: ConjugationTable = filter_conjugations(conjugation_all_table, args)

    print(f'{len(conjugations_filtered.records)} left')

    print()

    db_handler = ConjugationExerciseCSVHandler(CONJUGATION_EXERCISE_CSV_LOG_FILE_PATH, DEFAULT_USER_NAME)

    should_continue = True
    while should_continue and len(conjugations_filtered.records) > 0:
        verb = conjugations_filtered.random_record(rng)
        print(verb.summary())

        try:
            user_answer = input()
            is_correct = weak_equals(user_answer, verb.word)
            if is_correct:
                print('correct', end='\n\n')
                if not args.keep:
                    conjugations_filtered.records.remove(verb)
                    if len(conjugations_filtered.records) % 10 == 0:
                        print(f'{len(conjugations_filtered.records)} left\n')
            else:
                print(f'wrong. proper answer is {verb.word}', end='\n\n')
            db_handler.update_db(
                user=DEFAULT_USER_NAME,
                lang='latin',
                infinitive=verb.infinitive,
                mood=verb.mood,
                tense=verb.tense,
                voice=verb.voice,
                person=verb.person,
                number=verb.number,
                correct_form=verb.word,
                user_answer=user_answer,
                is_correct=is_correct
            )
        except KeyboardInterrupt:
            should_continue = False
            print('')

    print('terminating..')
