from lib.parsing_dict import *
from lib.utils import *

dicts_folder = 'dicts'
rng = default_rng()

# todo option to remove words displayed already
# todo or maybe option to decide after each word whether it should be removed or not
# todo bug (add tests):
# prop something up [phrasal
# prop something up [phrasal verb]
# They ran him up quick, and propped him out, over to leeward, and left him
# todo start from certain index (and stop at certain) -s -e
# and/or option to start/end at a certain word -a -z


if __name__ == "__main__":
    args = parse_args()
    dict_path = parse_dict_path(args.language, dicts_folder)

    raw_lines = read_file_raw(dict_path)
    dictionary = parse_english_dict(raw_lines) if args.language == 'english' else parse_latin_dict(raw_lines)

    user_input = 'y'
    while user_input.lower() != 'n': # proceed until user explicitly tells to stop
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
        print()
