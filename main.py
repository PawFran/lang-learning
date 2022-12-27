from lib.parsing_dict import *
from lib.utils import *

dict_path = 'dicts/latin.txt'
rng = default_rng()

if __name__ == "__main__":
    raw_lines = read_file_raw(dict_path)
    dictionary = parse_dict(raw_lines)

    user_input = 'y'
    while user_input.lower() != 'n':
        random_entry = random_dict_entry(dictionary)
        print(random_entry.head.base, end=' ')
        input('')
        print(random_entry.head.head_raw)
        print(random_entry.example, end=' ')
        input('')
        print(random_entry.translations, end=' ')
        user_input = input('\nProceed ? [y]/n\n')
