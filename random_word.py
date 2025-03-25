#!/usr/bin/env python3

import time

from synonyms.utils import SynonymFinder
from vocabulary.lib.parsing_dict import *

if __name__ == "__main__":
    args = parse_args()

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

    rng = default_rng()

    synonyms_number = 3

    continue_exercise = True
    while continue_exercise and dictionary is not None and dictionary.length() > 0:
        current_entry: DictionaryEntry = dictionary.random_dict_entry(rng)
        print(current_entry.head.head_raw)
        print(current_entry.example)

        continue_current_translation = True
        while continue_current_translation:
            translations_number = len(current_entry.translations)
            translations_left = translations_number
            last_translation = translations_left == 1
            print(f'translations left: {translations_left}')
            user_translation = input('translation: ')
            synonyms: list[str] = synonym_finder.similar_translations(user_translation, n=synonyms_number)
            for i in range(len(synonyms)):
                print(f'{i + 1}. {synonyms[i]}')
            user_choice = input('choose answer (digit) or try again (a) or skip (s) or terminate (t): ').strip()
            if user_choice == 'a':  # try again
                continue
            elif user_choice == 's':  # skip
                continue_current_translation = False
                print('all translations:')
                for i in range(len(current_entry.translations)):
                    print(f'{i + 1}. {current_entry.translations[i]}')
                dictionary.remove_entry(current_entry)
                if dictionary.length() % 10 == 0:
                    print(f'words left in dictionary: {dictionary.length()}', end='\n\n')
            elif user_choice == 't':  # terminate
                continue_current_translation = False
                continue_exercise = False
            elif user_choice.isdigit():  # answer
                user_answer = synonyms[int(user_choice) - 1]
                if user_answer in current_entry.translations:
                    print('correct', end='\n\n')
                    continue_current_translation = not last_translation
                    dictionary.remove_single_translation(current_entry, user_answer)
                    if dictionary.length() % 10 == 0:
                        print(f'words left in dictionary: {dictionary.length()}', end='\n\n')
                else:
                    print('wrong. try again')
            else:
                print('invalid response. try again')

    if dictionary is None or dictionary.length() == 0:
        print('no words left')
    print('terminating..')
