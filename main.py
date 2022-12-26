from parsing_dict import *

dict_path = 'latin_test.txt'
# TODO validate entry file:
# each entry is:
# head
# example
# list of translations
# then blank line (or many) or end of the file

if __name__ == "__main__":
    raw_lines = read_file_raw(dict_path)
    print(raw_lines)
    for group in group_raw_lines(raw_lines):
        print(parse_dict_entry(group))
        print('====')
