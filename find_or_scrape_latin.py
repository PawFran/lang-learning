#!/usr/bin/env python

from vocabulary.lib.parsing_dict import *
import sys
from collections import namedtuple
from scraping.lib.utils import get_scraped_data, print_scraping_results, output_temporary_file_name, print_and_return

FOUND_HEADER = '### found ###\n'
SCRAPED_HEADER = '### scraped ###\n'

def find_or_scrape(words: list[str]) -> str:
    Args = namedtuple('Args', ['language', 'start_word', 'end_word'])
    args = Args('latin', None, None)

    dictionary: Dictionary = parse_dictionary(args)

    entries_found: list[DictionaryEntry] = []
    words_initially_not_found: list[str] = []
    entries_finally_not_found: [DictionaryEntry] = []

    for input_word in words:
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

    output_placeholder = ''

    if len(entries_found) > 0:
        output_placeholder += print_and_return(FOUND_HEADER)
        for entry in entries_found:
            output_placeholder += print_and_return(entry.head.head_raw)
            output_placeholder += print_and_return(f'({entry.example})')
            for i in range(len(entry.translations)):
                output_placeholder += print_and_return(f'{i + 1}. {entry.translations[i]}')
            output_placeholder += print_and_return('')

    if len(entries_finally_not_found) > 0:
        output_placeholder += print_and_return(SCRAPED_HEADER)
        with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
            output_placeholder += print_scraping_results(f, entries_finally_not_found)

    return output_placeholder


if __name__ == '__main__':
    words = sys.argv[1:]
    find_or_scrape(words)
