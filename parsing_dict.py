from classes import *


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


def parse_dict_entry(single_group_of_lines):
    first_line = single_group_of_lines[0]
    example = single_group_of_lines[1].strip()
    translations = [x.strip() for x in single_group_of_lines[2:]]

    if Verb.is_verb(first_line):
        dict_entry_head = Verb.from_entry_head(first_line)
        return DictEntry(dict_entry_head, example, translations)
    elif Noun.is_noun(first_line):
        dict_entry_head = Noun.from_entry_head(first_line)
        return DictEntry(dict_entry_head, example, translations)
    elif Adverb.is_adverb(first_line):
        dict_entry_head = Adverb.from_entry_head(first_line)
        return DictEntry(dict_entry_head, example, translations)
    elif Adjective.is_adjective(first_line):
        dict_entry_head = Adjective.from_entry_head(first_line)
        return DictEntry(dict_entry_head, example, translations)
