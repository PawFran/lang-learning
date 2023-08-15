from vocabulary.lib.parsing_dict import *
import sys
from collections import namedtuple

if __name__ == '__main__':
    Args = namedtuple('Args', ['language', 'start_word', 'end_word'])
    args = Args('latin', None, None)

    dictionary: Dictionary = parse_dictionary(args)

    entries_found: list[DictionaryEntry] = []
    words_not_found: list[str] = []

    for input_word in sys.argv[1:]:
        query_result = dictionary.find_by_header_using_weak_compare(input_word)
        if len(query_result) > 0:
            entries_found += query_result
        else:
            words_not_found.append(input_word)

    print('### found ###\n')
    for entry in entries_found:
        print(entry.head.head_raw)
        print(f'({entry.example})')
        for i in range(len(entry.translations)):
            print(f'{i+1}.{entry.translations[i]}')
        print('')

    if len(words_not_found) > 0:
        print('### scraping ###')
        scraper_args = ' '.join(words_not_found)
        os.system(f'python scrape_latin_dict.py {scraper_args}')
