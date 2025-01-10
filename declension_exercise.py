# when third declension is mentioned all variants should be included
# todo filter by word

import copy
import os

from numpy.random import default_rng

from actions.declension import DECLENSION_EXERCISE_CSV_LOG_FILE_PATH, DECLENSION_SESSION_METADATA_CSV_PATH
from common.lib.utils import weak_equals, DEFAULT_USER_NAME
from declension.lib.parsing_args import *
from declension.lib.utils import *
from vocabulary.lib.file_db import DeclensionExerciseCSVHandler, DeclensionExerciseSessionMetadataCSVHandler

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

    db_handler = DeclensionExerciseCSVHandler(DECLENSION_EXERCISE_CSV_LOG_FILE_PATH, DEFAULT_USER_NAME)
    session_metadata_handler = DeclensionExerciseSessionMetadataCSVHandler(
        path=DECLENSION_SESSION_METADATA_CSV_PATH,
        session_id=db_handler.current_session_id,
        user_name=DEFAULT_USER_NAME,
        declensions_included={d.type.value for d in declensions_filtered.declensions}
    )

    should_continue = True
    interrupted = False
    while should_continue:
        backup_dict = copy.deepcopy(current_dict)  # in case remove is on and answer is wrong
        pop = False if args.keep else True
        declension_test: DeclensionTest = random_declension_entry(current_dict, rng,
                                                                  pop)  # here current_dict may be modified
        if declension_test is None:
            should_continue = False  # means all entries were already removed
        else:
            declension_prompt: DeclensionPrompt = declension_test.prompt
            print(declension_prompt.base_word, declension_prompt.case, declension_prompt.number)

            try:
                user_answer = input()
                is_correct = weak_equals(user_answer, declension_test.answer)
                if is_correct:
                    print('correct', end='\n\n')
                else:
                    print(f'wrong. proper answer is {declension_test.answer}', end='\n\n')
                    current_dict = backup_dict

                db_handler.update_db(user=DEFAULT_USER_NAME,
                                     lang='latin',
                                     base_word=declension_prompt.base_word,
                                     number=declension_prompt.number,
                                     case=declension_prompt.case,
                                     correct_form=declension_test.answer,
                                     user_answer=user_answer,
                                     is_correct=is_correct)
            except (KeyboardInterrupt, EOFError):
                should_continue = False
                interrupted = True
                session_metadata_handler.update(interrupted=True)
                print('')

        if not args.keep:
            current_length = current_dict.length()
            if current_length % 10 == 0:
                print(f'current nr of entries: {current_length}\n')

    if not interrupted:
        session_metadata_handler.update(interrupted=False)

    print('terminating..')
