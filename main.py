from lib.parsing_dict import *
from lib.utils import *

latin_dict_path = 'dicts/latin.txt'
english_dict_path = 'dicts/english.txt'
rng = default_rng()

if __name__ == "__main__":
    #raw_lines = read_file_raw(latin_dict_path)
    #dictionary = parse_latin_dict(raw_lines)

    raw_lines = read_file_raw(english_dict_path)
    dictionary = parse_english_dict(raw_lines)

    user_input = 'y'
    while user_input.lower() != 'n':
        random_entry = random_dict_entry(dictionary)
        print(random_entry.head.base, end=' ')
        input('')
        print(random_entry.head.head_raw)
        print(random_entry.example, end=' ')
        input('')
        for i in range(len(random_entry.translations)):
            print(f'{i+1}. {random_entry.translations[i]}')
        user_input = input('\nProceed ? [y]/n\n')
