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
        try:
            print(rng.choice(entry.translations))
        except ValueError:
            print(f'cannot find translation for base {base}')  # todo debug

        answer = input('translation: ')

        if weak_compare(answer, base):
            print('correct')
            if args.remove:
                dictionary.remove(entry)
        else:
            print(f'wrong. correct answer is {base}')

        print('')

        # user_input = input('\nProceed ? [y]/n\n').strip()

        # todo ask about all possible forms and translations

    print('terminating..')
