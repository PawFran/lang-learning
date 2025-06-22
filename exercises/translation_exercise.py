#!/usr/bin/env python3

from sqlalchemy import text
from sqlalchemy.orm import Session

import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from actions.translation import TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH, TRANSLATION_SESSION_METADATA_CSV_PATH
from common.lib.utils import DEFAULT_USER_NAME
from database.db_classes import TranslationLastUninterruptedSessionHardWords
from database.initialize_db import default_db_initialization
from environment.setup import engine
from vocabulary.lib.parsing_dict import *
from vocabulary.lib.utils import compare_answer_with_full_head_raw, shortcuts_summary

# todo option to take only a number or percentage of the words ranked highest (in terms of probability)

if __name__ == '__main__':
    args = parse_args()

    if args.language is None:
        args.language = 'latin'
        print(f'no language chosen. {args.language} will be used as default')

    if args.user_name is None:
        args.user_name = DEFAULT_USER_NAME

    print(f'logged as {args.user_name}')

    if args.revise_last_session is None:
        args.revise_last_session = False

    if args.revise_last_session:
        args.start_word = None
        args.end_word = None
        args.filter = None

    dictionary: Dictionary = parse_dictionary(args)

    if args.filter is not None:
        dictionary = dictionary.filter_by_complex_condition(args.filter)

    if args.revise_last_session:
        print('revising last session, arguments like start/end word and filtered parts of speech are ignored')
        with Session(engine) as session:
            hard_words = session.execute(text(TranslationLastUninterruptedSessionHardWords.__view_query__)).all()
            if len(hard_words) > 0:
                print(f"Found {len(hard_words)} difficult words from last session to review")
            else:
                print("No difficult words found from last session")

        # Filter dictionary to only include words that were difficult in last session
        filtered_entries = []
        for word in hard_words:
            found = False
            for entry in dictionary.entries:
                if entry.head.header_without_metadata() == word.header:
                    filtered_entries.append(entry)
                    found = True
            if not found:
                print(f'''couldn't find {word.header} in dictionary''')
        dictionary = Dictionary(entries=filtered_entries, lang=dictionary.lang)

    db_handler = TranslationExerciseCSVHandler(TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH, args.user_name)
    session_metadata_handler = TranslationExerciseSessionMetadataCSVHandler(
        path=TRANSLATION_SESSION_METADATA_CSV_PATH,
        session_id=db_handler.current_session_id,
        user_name=args.user_name,
        revise_last_session=args.revise_last_session,
        start_word=args.start_word,
        end_word=args.end_word,
        filtered_parts_of_speech=args.filter
    )

    rng = default_rng()

    print(f'remember about shortcuts {shortcuts_summary}')

    print(f'number of translations in dictionary: {dictionary.translations_nr()}', end='\n\n')

    should_continue = True
    interrupted = False
    while should_continue and dictionary is not None and dictionary.translations_nr() > 0:
        if args.user_name is not None:
            random_word_with_translation = dictionary.smart_random_dict_entry_with_translation(db_handler,
                                                                                               user=args.user_name,
                                                                                               n_times=20,
                                                                                               rng=rng)  # todo in the future parameterize it ?
        else:
            random_word_with_translation = dictionary.random_entry_with_translation(rng)

        entry = random_word_with_translation.entry
        word_pl = random_word_with_translation.translation

        head_no_metadata = entry.head.head_raw.split('[')[0]

        print(word_pl)

        try:
            answer = input('translation: ').strip()

            is_correct = compare_answer_with_full_head_raw(entry.head.head_raw, answer)

            if is_correct:
                print(f'correct ({entry.head.head_raw}) \n({entry.example})')
                if not args.keep:
                    dictionary.remove_single_translation(entry, word_pl)
                    if dictionary.translations_nr() % 10 == 0:
                        print(f'\n{dictionary.translations_nr()} translations left in dict')
            else:
                print(f'wrong. correct answer is "{entry.head.head_raw}" ({entry.example})')
                # todo if another translation from dict was given print it's meaning - not that easy. it may be in original dict but not after some removals
                # actually some translations may be unequivocal (ex. także -> etiam, quoque)

            if args.user_name is not None:
                db_handler.update_db(user=args.user_name, word_pl=word_pl,
                                     lang=args.language, translation=head_no_metadata,
                                     was_correct=is_correct, user_answer=answer)

            print('')

            # todo ask about all possible forms and translations
        except (KeyboardInterrupt, EOFError):
            should_continue = False
            interrupted = True
            session_metadata_handler.update(interrupted=True)
            print('\n')

    if not interrupted:
        session_metadata_handler.update(interrupted=False)
        default_db_initialization()

    print('terminating..')
