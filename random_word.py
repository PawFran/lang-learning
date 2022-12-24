from classes import *
import re


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


def extract_from_square_brackets(pattern, line):
    match = re.search(pattern, line)
    if match is not None:
        return match.group().replace('[', '').replace(']',
                                                      '')  # should be possible by using some groups in re directly ?
    else:
        return None


def conjugation(dict_entry_head):
    # conjugation may be [I] or [II] or [III] or [IIIa] or [IV]
    conjugation_pattern = '\[I{1,3}V*\]'
    return extract_from_square_brackets(conjugation_pattern, dict_entry_head)


def declension(dict_entry_head):
    # declension may be [I] or [II] or [III vowel] or [III consonant] or [III mixed] or [IV] or [V]
    declension_pattern = '\[I{0,3} *(vowel)*(consonant)*(mixed)*V*\]'
    return extract_from_square_brackets(declension_pattern, dict_entry_head)


def only_plural(dict_entry_head):
    return '[pl]' in dict_entry_head


def parse_dict_entry(single_group_of_lines):
    entry = DictEntry(word=single_group_of_lines[0],
                      example=single_group_of_lines[1],
                      translations=single_group_of_lines[2:])
    # head = dict_entry[0]  # what if there's no head
    example = None  # what if there's no example
    translation = None  # what if there's no translation

    # use regex for both determining form and declension/conjugation

    # TODO this part could be moved to class' internals
    if '[verb]' in head.lower():
        forms = head.split(' [')[0]
        parsed = Verb(base=forms[0], conjugation='???', infinite=forms[1],
                      perfect=forms[2], supine=forms[3])  # what if there's no one of the forms ?
    elif 'noun' in head.lower():
        pass
