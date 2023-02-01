from lib.parsing_args import parse_args, parse_dict_path
from lib.parsing_dict import *
from lib.utils import *

dicts_folder = 'dicts'
rng = default_rng()

if __name__ == "__main__":
    args = parse_args()
    dict_path = parse_dict_path(args.language, dicts_folder)

    raw_lines = read_file_raw(dict_path)
    dictionary = parse_english_dict(raw_lines, args.start_word, args.end_word) \
        if args.language == 'english' \
        else parse_latin_dict(raw_lines, args.start_word, args.end_word)

    user_input = 'y'
    while user_input.lower() != 'n' and dictionary is not None and dictionary.length() > 0:  # proceed until user explicitly tells to stop
        current_entry = random_dict_entry(dictionary)
        print(current_entry.head.base, end=' ')
        input('')
        print(current_entry.head.head_raw)
        print(current_entry.example, end=' ')
        input('')
        for i in range(len(current_entry.translations)):
            print(f'{i + 1}. {current_entry.translations[i]}')
        if args.remove:
            whats_next = input(
                '\nWhat do you want: [1] remove word and proceed (default) [2] keep word and proceed [3] terminate ?\n').strip()
            if whats_next == '2':
                user_input = 'y'
            elif whats_next == '3':
                user_input = 'n'
            else:
                dictionary.remove(current_entry)
        else:
            user_input = input('\nProceed ? [y]/n\n').strip()

    if dictionary is None or dictionary.length() == 0:
        print('no words left in dictionary')
    print('terminating..')
