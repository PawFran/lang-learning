import sys
import logging

from scraping.lib.utils import *

output_temporary_file_name = 'scraping_out_tmp.txt'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('must give at least one argument (word to be found)')

    base_dict_URL = 'https://www.online-latin-dictionary.com/latin-english-dictionary.php'
    base_flexion_URL = 'https://www.online-latin-dictionary.com/latin-dictionary-flexion.php'

    deepl_headers = {
        'Authorization': 'DeepL-Auth-Key 0346e75c-3679-c5ed-4ac4-260beade18db:fx',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    scraper = LatinDictScraper(base_dict_URL, base_flexion_URL, deepl_headers)

    with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
        for input_word in sys.argv[1:]:

            try:
                scrape_result = scrape(scraper, input_word)
                word, grammatical_info, polish_translations = scrape_result.word, scrape_result.grammatical_info, \
                    scrape_result.polish_translations

                msg = parse_msg(scraper, input_word, word, grammatical_info)

                print_and_write(f, word)
                print_and_write(f, msg)
                print_and_write(f, '()\n')

                for t, i in zip(polish_translations, range(len(polish_translations))):
                    print_and_write(f, f'{i + 1}. {t}\n')

                print_and_write(f, '\n')

            except Exception as Argument:
                # print(f'cannot scrape {input_word}')
                logging.exception(f'cannot scrape {input_word}')
                print()
