#!/usr/bin/env python

from vocabulary.lib.parsing_dict import *
import sys
from collections import namedtuple
from scraping.lib.utils import get_scraped_data, print_scraping_results, output_temporary_file_name

if __name__ == '__main__':
    Args = namedtuple('Args', ['language', 'start_word', 'end_word'])
    args = Args('latin', None, None)

    dictionary: Dictionary = parse_dictionary(args)

    entries_found: list[DictionaryEntry] = []
    words_initially_not_found: list[str] = []
    entries_finally_not_found: [DictionaryEntry] = []

    for input_word in sys.argv[1:]:
        query_result = dictionary.find_by_word_using_weak_compare(input_word)
        if len(query_result) > 0:
            entries_found += query_result
        else:
            words_initially_not_found.append(input_word)

    if len(words_initially_not_found) > 0:
        scraped: [DictionaryEntry] = get_scraped_data(words_initially_not_found)

        # check again if not found (maybe another form, not in header, was in the input ex. abl sing)
        for entry in scraped:
            query_result: [DictionaryEntry] = dictionary.find_by_full_header_using_weak_compare(entry.head.head_raw)
            if len(query_result) > 0:
                for entry_found in query_result:
                    entries_found.append(entry_found)
            else:
                entries_finally_not_found.append(entry)

    if len(entries_found) > 0:
        print('### found ###\n')
        for entry in entries_found:
            print(entry.head.head_raw)
            print(f'({entry.example})')
            for i in range(len(entry.translations)):
                print(f'{i + 1}. {entry.translations[i]}')
            print('')

    if len(entries_finally_not_found) > 0:
        print('### scraped ###\n')
        with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
            print_scraping_results(f, entries_finally_not_found)
