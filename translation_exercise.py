from vocabulary.lib.db import *
from vocabulary.lib.parsing_dict import *
from vocabulary.lib.utils import *

if __name__ == '__main__':
    args = parse_args()
    dictionary = parse_dictionary(args)

    db_path = os.path.join('vocabulary', 'db', 'translation_exercise_results.csv')
    db_handler = TranslationExerciseDBHandler(db_path)

    rng = default_rng()

    print(f'number of words in dictionary: {dictionary.length()}', end='\n\n')

    user_input = 'y'
    while user_input.lower() != 'n' and dictionary is not None and dictionary.length() > 0:
        entry = random_dict_entry(dictionary, rng)

        word_original = entry.head.base

        word_pl = rng.choice(entry.translations)
        print(word_pl)

        answer = input('translation: ')

        is_correct = weak_equals(answer, word_original)

        if is_correct:
            print('correct')
            if args.remove:
                dictionary.remove(entry)
        else:
            print(f'wrong. correct answer is {word_original}')

        if args.user_name is not None:
            db_handler.update_db(user=args.user_name, word_pl=word_pl,
                                 lang=args.language, translation=word_original,
                                 was_correct=is_correct)

        print('')

        # todo ask about all possible forms and translations

    print('terminating..')
