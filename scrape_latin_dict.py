import sys
import logging

from scraping.lib.utils import *

output_temporary_file_name = 'scraping_out_tmp.txt'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('must give at least one argument (word to be found)')

    scraper = LatinDictScraper(base_dict_URL, base_flexion_URL, deepl_headers)

    with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
        for input_word in sys.argv[1:]:

            try:
                results = scrape(scraper, input_word)

                for scrape_result in results:
                    print_output(f, scraper, input_word, scrape_result)

            except Exception as Argument:
                # print(f'cannot scrape {input_word}')
                logging.exception(f'cannot scrape {input_word}')
                print()
