import re

from vocabulary.lib.dict_classes import *


def read_file_raw(path):
    with open(path, encoding="utf8") as f:
        lines_raw = f.readlines()
    return lines_raw


def group_raw_lines(raw_lines):
    groups = []
    single_group = []
    for line in raw_lines:
        if line != '\n':  # '\n' is a groups separator
            single_group.append(line)
        else:
            groups.append(single_group)
            single_group = []
    if len(single_group) > 0:  # if there's no '\n' at the end last append must be forced
        groups.append(single_group)
    return groups


def parse_example(example_raw):
    example_stripped = example_raw.strip()
    if example_stripped.startswith('('):
        return example_stripped[1:-1]
    else:
        return example_stripped


def parse_translation(translation_raw):
    end = re.search('[1-9]+', translation_raw).end()
    return translation_raw[end + 1:].strip()


def parse_single_group_of_lines(single_group_of_lines):
    first_line = single_group_of_lines[0].strip()
    example = parse_example(single_group_of_lines[1])
    translations = [parse_translation(x) for x in single_group_of_lines[2:]]

    return first_line, example, translations


def parse_latin_dict_entry(single_group_of_lines):
    first_line, example, translations = parse_single_group_of_lines(single_group_of_lines)

    if LatinVerb.is_verb(first_line):
        dict_entry_head = LatinVerb.from_entry_head(first_line)
        return DictionaryEntry(dict_entry_head, example, translations)
    elif LatinNoun.is_noun(first_line):
        dict_entry_head = LatinNoun.from_entry_head(first_line)
        return DictionaryEntry(dict_entry_head, example, translations)
    elif LatinAdverb.is_adverb(first_line):
        dict_entry_head = LatinAdverb.from_entry_head(first_line)
        return DictionaryEntry(dict_entry_head, example, translations)
    elif LatinAdjective.is_adjective(first_line):
        dict_entry_head = LatinAdjective.from_entry_head(first_line)
        return DictionaryEntry(dict_entry_head, example, translations)


def parse_english_dict_entry(single_group_of_lines):
    first_line, example, translations = parse_single_group_of_lines(single_group_of_lines)

    dict_entry_head = EnglishWord.from_entry_head(first_line)
    return DictionaryEntry(dict_entry_head, example, translations)


def dict_subset(dictionary, start_word=None, end_word=None):
    start_index = dictionary.weak_index(start_word) if start_word is not None else 0
    end_index = dictionary.weak_index(end_word) if end_word is not None else dictionary.length() - 1

    if start_index is None:
        print(f'cannot find {start_word}')
        return None
    if end_index is None:
        print(f'cannot find {end_word}')
        return None

    if start_index > end_index:
        print('start is after end - cannot take reasonable subset')
        return None

    entries_subset = dictionary.entries[start_index: end_index + 1]
    return Dictionary(entries_subset)


def parse_dict(raw_lines, parser_for_dict_entry, start_word=None, end_word=None):
    raw_lines_grouped = group_raw_lines(raw_lines)

    dictionary = Dictionary(list())
    for single_group in raw_lines_grouped:
        dict_entry = parser_for_dict_entry(single_group)
        dictionary.append(dict_entry)

    return dict_subset(dictionary, start_word, end_word)


def parse_latin_dict(raw_lines, start_word=None, end_word=None):
    return parse_dict(raw_lines, parse_latin_dict_entry, start_word=start_word, end_word=end_word)


def parse_english_dict(raw_lines, start_word=None, end_word=None):
    return parse_dict(raw_lines, parse_english_dict_entry, start_word=start_word, end_word=end_word)
