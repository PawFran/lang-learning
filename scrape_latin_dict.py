#!/usr/bin/env python

import logging
import sys

from scraping.lib.utils import *
from vocabulary.lib.dict_classes import DictionaryEntry

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('must give at least one argument (word to be found)')

    scraper = LatinDictScraper(base_dict_URL, base_flexion_URL, deepl_headers)

    with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
        for input_word in sys.argv[1:]:

            try:
                results: list[DictionaryEntry] = scrape(scraper, input_word)

                print_scraping_results(f, results)

            except Exception as Argument:
                # print(f'cannot scrape {input_word}')
                logging.exception(f'cannot scrape {input_word}')
                print()
