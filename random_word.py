from vocabulary.lib.parsing_dict import *

# todo return error when no language is set (or provide default and inform about it)

if __name__ == "__main__":
    args = parse_args()

    dictionary = parse_dictionary(args)

    print(f'number of words in dictionary: {dictionary.length()}', end='\n\n')

    rng = default_rng()

    user_input = 'y'
    while user_input.lower() != 'n' and dictionary is not None and dictionary.length() > 0:  # proceed until user explicitly tells to stop
        current_entry = dictionary.random_dict_entry(rng)
        print(current_entry.head.base, end=' ')
        input('')
        print(current_entry.head.head_raw)
        print(current_entry.example, end=' ')
        input('')
        for i in range(len(current_entry.translations)):
            print(f'{i + 1}. {current_entry.translations[i]}')
        if args.remove:
            whats_next = input(
                '''\n[1] remove word (default) [2] keep word [3] terminate\n'''
            ).strip()
            if whats_next == '2':
                user_input = 'y'
            elif whats_next == '3':
                user_input = 'n'
            else:
                dictionary.remove_entry(current_entry)
                if dictionary.length() % 10 == 0:
                    print(f'words left in dictionary: {dictionary.length()}', end='\n\n')
        else:
            user_input = input('\nProceed ? [y]/n\n').strip()

    if dictionary is None or dictionary.length() == 0:
        print('no words left')
    print('terminating..')
