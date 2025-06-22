import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actions.conjugation import CONJUGATION_EXERCISE_CSV_LOG_FILE_PATH, \
    CONJUGATION_EXERCISE_SESSION_METADATA_CSV_LOG_FILE_PATH
from common.lib.utils import weak_equals, DEFAULT_USER_NAME
from conjugation.lib.conjugation_classes import *
from conjugation.lib.parsing_args import parse_args
from conjugation.lib.utils import filter_conjugations
from database.initialize_db import default_db_initialization
from vocabulary.lib.file_db import ConjugationExerciseCSVHandler, ConjugationExerciseSessionMetadataCSVHandler

if __name__ == '__main__':
    rng = default_rng()
    json_file_path = os.path.join("../conjugation", "resources", "conjugation.json")

    args = parse_args()

    conjugation_all_table = ConjugationTable.from_file_path(json_file_path)
    conjugations_filtered: ConjugationTable = filter_conjugations(conjugation_all_table, args)

    conjugations_included = {c.conjugation_type.value for c in conjugations_filtered.records}
    moods_included = {c.mood.value for c in conjugations_filtered.records}
    tenses_included = {c.tense.value for c in conjugations_filtered.records}
    voices_included = {c.voice.value for c in conjugations_filtered.records}

    print()
    print('exercise summary:')
    for x in [conjugations_included, moods_included, tenses_included, voices_included]:
        print(x)
    print()

    print(f'{len(conjugations_filtered.records)} left')

    print()

    db_handler = ConjugationExerciseCSVHandler(CONJUGATION_EXERCISE_CSV_LOG_FILE_PATH, DEFAULT_USER_NAME)
    session_metadata_handler = ConjugationExerciseSessionMetadataCSVHandler(
        path=CONJUGATION_EXERCISE_SESSION_METADATA_CSV_LOG_FILE_PATH,
        session_id=db_handler.current_session_id,
        user_name=DEFAULT_USER_NAME,
        conjugations_included=conjugations_included,
        moods_included=moods_included,
        tenses_included=tenses_included,
        voices_included=voices_included
    )

    should_continue = True
    interrupted = False
    while should_continue and len(conjugations_filtered.records) > 0:
        verb = conjugations_filtered.random_record(rng)
        # do not tell about form when it's always the same in particular exercise
        # summary = verb.summary(mood=len(moods_included) > 1, tense=len(tenses_included) > 1, voice=len(voices_included) > 1)
        summary = verb.summary()
        print(summary)

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
        default_db_initialization()

    print('terminating..')
