from vocabulary.lib.parsing_dict import *
from vocabulary.lib.utils import *


if __name__ == '__main__':
    args = parse_args()
    dictionary = parse_dictionary(args)

    rng = default_rng()

    print(f'number of words in dictionary: {dictionary.length()}', end='\n\n')

    user_input = 'y'
    while user_input.lower() != 'n' and dictionary is not None and dictionary.length() > 0:

        entry = random_dict_entry(dictionary, rng)

        base = entry.head.base
        translation = rng.choice(entry.translations)

        print(translation)

        answer = input('translation: ')
        if weak_compare(answer, base):
            print('correct')
        else:
            print(f'wrong. correct answer is {translation}')

        user_input = input('\nProceed ? [y]/n\n').strip()

        # ask about all possible forms and translations

    print('terminating..')
