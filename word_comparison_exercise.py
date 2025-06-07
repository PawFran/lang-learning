import os

WORD_COMPARISON_PATH = os.path.join(os.path.dirname(__file__), 'vocabulary', 'dicts', 'word_comparison.txt')


def clean_words(lines_raw):
    words_split = [line.split('vs') for line in lines_raw]
    return [ list(map(str.strip, words_set)) for words_set in words_split]


if __name__ == '__main__':
    with open(WORD_COMPARISON_PATH) as f:
        word_comparison_lines_raw = [line.strip() for line in f.readlines()]

    words_to_compare = clean_words(word_comparison_lines_raw)
    for word in words_to_compare: print(word)