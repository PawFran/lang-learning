import os

from actions.conjugation import CONJUGATION_EXERCISE_CSV_LOG_FILE_PATH, CONJUGATION_EXERCISE_SESSION_METADATA_CSV_LOG_FILE_PATH
from common.lib.utils import weak_equals, DEFAULT_USER_NAME
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args
from conjugation.lib.utils import filter_conjugations
from vocabulary.lib.file_db import ConjugationExerciseCSVHandler, ConjugationExerciseSessionMetadataCSVHandler

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("conjugation", "resources", "conjugation.json")

    args = parse_args()

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)
    conjugations_filtered: ConjugationTable = filter_conjugations(conjugation_all_table, args)

    print(f'{len(conjugations_filtered.records)} left')

    print()

    db_handler = ConjugationExerciseCSVHandler(CONJUGATION_EXERCISE_CSV_LOG_FILE_PATH, DEFAULT_USER_NAME)
    session_metadata_handler = ConjugationExerciseSessionMetadataCSVHandler(
        path=CONJUGATION_EXERCISE_SESSION_METADATA_CSV_LOG_FILE_PATH,
        session_id=db_handler.current_session_id,
        user_name=DEFAULT_USER_NAME,
        conjugations_included=args.conjugations,
        moods_included=args.moods,
        tenses_included=args.tenses,
        voices_included=args.voices
        )

    should_continue = True
    interrupted = False
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
                mood=verb.mood.value,
                tense=verb.tense.value,
                voice=verb.voice.value,
                person=verb.person.value,
                number=verb.number.value,
                correct_form=verb.word,
                user_answer=user_answer,
                is_correct=is_correct
            )
        except (KeyboardInterrupt, EOFError):
            should_continue = False
            interrupted = True
            session_metadata_handler.update(interrupted=True)
            print('')
            print('interrupting..')

    if not interrupted:
        session_metadata_handler.update(interrupted=False)
    print('terminating..')
