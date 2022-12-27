from lib.parsing_dict import *

dict_path = 'dicts/latin.txt'

if __name__ == "__main__":
    raw_lines = read_file_raw(dict_path)
    raw_lines_grouped = group_raw_lines(raw_lines)
    for group in raw_lines_grouped:
        print(parse_dict_entry(group))
        print('====')
