from lib.parsing_dict import *

dict_path = 'dicts/latin.txt'

if __name__ == "__main__":
    raw_lines = read_file_raw(dict_path)
    dictionary = parse_dict(raw_lines)
    for entry in dictionary.entries:
        print(entry)
        print('====')
