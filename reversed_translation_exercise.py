#!/usr/bin/env python3

import time

from actions.translation import REVERSED_TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH, REVERSED_TRANSLATION_SESSION_METADATA_CSV_PATH
from common.lib.utils import DEFAULT_USER_NAME
from database.initialize_db import default_db_initialization
from synonyms.utils import SynonymFinder
from vocabulary.lib.parsing_dict import *
from utils.lib.utils import print_all, is_proper_answer, answer_parsed

if __name__ == "__main__":
    args = parse_args()

    synonyms_number = 3

    if args.user_name is None:
        args.user_name = DEFAULT_USER_NAME

    if args.language is None:
        args.language = 'latin'
        print(f'no language chosen. {args.language} will be used as default')

    dictionary: Dictionary = parse_dictionary(args)
    if args.filter is not None:
        dictionary = dictionary.filter_by_complex_condition(args.filter)

    print(f'number of words in dictionary: {dictionary.length()}', end='\n\n')

    print('Initializing synonyms finder...')
    start_time = time.time()
    synonym_finder = SynonymFinder()
    end_time = time.time()
    print(f'Synonyms finder initialized in {end_time - start_time:.1f} seconds', end='\n\n')

    db_handler = ReversedTranslationExerciseCSVHandler(REVERSED_TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH, args.user_name, args.language)
    session_metadata_handler = TranslationExerciseSessionMetadataCSVHandler(
        path=REVERSED_TRANSLATION_SESSION_METADATA_CSV_PATH,
        session_id=db_handler.current_session_id,
        user_name=args.user_name,
        revise_last_session=args.revise_last_session,
        start_word=args.start_word,
        end_word=args.end_word,
        filtered_parts_of_speech=args.filter
    )

    rng = default_rng()

    continue_exercise = True
    interrupted = False
    while continue_exercise and dictionary is not None and dictionary.length() > 0:
        current_entry: DictionaryEntry = dictionary.random_dict_entry(rng)
        full_header = current_entry.head.head_raw
        translations_number = len(current_entry.translations)
        print(full_header)
        print(current_entry.example)

        continue_current_translation = True
        while continue_current_translation:
            translations_left = len(current_entry.translations)
            last_translation = translations_left == 1
            
            print(f'translations left: {translations_left}')

            try:
                user_translation = input('translation: ')
                
                synonyms: list[str] = synonym_finder.similar_translations(user_translation, n=synonyms_number)
                print_all(synonyms)
                user_choice = input('choose answers (digits separated by space) or try again (a) or skip (s) or terminate (t): ').strip()
                
                if user_choice == 'a':  # try again
                    continue
                elif user_choice == 's':  # skip
                    is_correct = False
                    continue_current_translation = False

                    print('')
                    print('all remaining translations:')
                    print_all(current_entry.translations)
                    print('')
                    
                    db_handler.update_db(head_raw=full_header,
                                        example=current_entry.example,
                                        number_of_translations_total=translations_number, 
                                        translations_left=current_entry.translations, 
                                        user_answer="", was_correct=is_correct)

                    for translation in current_entry.translations:
                        dictionary.remove_single_translation(current_entry, translation)

                    if dictionary.length() % 10 == 0:
                        print(f'words left in dictionary: {dictionary.length()}', end='\n\n')
                elif user_choice == 't':  # terminate
                    continue_current_translation = False
                    continue_exercise = False
                elif is_proper_answer(user_choice):  # answer
                    user_answers = [synonyms[int(x) - 1] for x in answer_parsed(user_choice)]

                    correct_answers =   [answer for answer in user_answers if answer in     current_entry.translations]
                    incorrect_answers = [answer for answer in user_answers if answer not in current_entry.translations]

                    for answer in correct_answers:
                        print(f'"{answer}" is correct', end='\n\n')
                        
                        continue_current_translation = not last_translation

                        db_handler.update_db(head_raw=full_header,
                                             example=current_entry.example,
                                             number_of_translations_total=translations_number,
                                             translations_left=current_entry.translations,
                                             user_answer=answer, was_correct=True)

                        dictionary.remove_single_translation(current_entry, answer)
                    if dictionary.length() % 10 == 0:
                        print(f'words left in dictionary: {dictionary.length()}', end='\n\n')

                    for answer in incorrect_answers:
                        print(f'"{answer}" is wrong', end='\n\n')

                        db_handler.update_db(head_raw=full_header,
                                             example=current_entry.example,
                                             number_of_translations_total=translations_number,
                                             translations_left=current_entry.translations,
                                             user_answer=answer, was_correct=False)
                else:
                    print('invalid response. try again')
            except Exception as e:
                print(f'Exception occurred: {e}')
                continue_exercise = False
                interrupted = True
                session_metadata_handler.update(interrupted=True)
                print('\n')

    if dictionary is None or dictionary.length() == 0:
        print('no words left')

    if not interrupted:
        session_metadata_handler.update(interrupted=False)
    
    default_db_initialization()

    print('terminating..')
