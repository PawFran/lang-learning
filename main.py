from random_word import *

dict_path = 'latin_test.txt'
# TODO validate dict file (and other files in the future)

if __name__ == "__main__":
    raw_lines = read_file_raw(dict_path)
    print(raw_lines)
    print(group_raw_lines(raw_lines))
