import re
import sys
import logging

from scraping.lib.latin_scraper import *

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


    def print_and_write(text):
        print(text, end='')
        f.write(text)


    def scrape():
        soup = scraper.get_dict_soup(input_word)

        results = soup.find(id="myth")
        if results is None:
            all_links = soup.find_all('a', href=True)
            links_with_words = [link for link in all_links if 'lemma' in link['href']]
            # usually this word is given with additional info, ex. "castīgo (tr. v. I conjug.)"
            new_word = links_with_words[0].text.split(' ')[0]
            # todo what if no reasonable prompt was given ?

            soup = scraper.get_dict_soup(new_word)
            results = soup.find(id="myth")
            if results is None:
                # should never happen, but still..
                raise Exception(f'''couldn't find translation for neither {input_word} nor {new_word}''')

        word = results.find_all("span", class_="lemma")[0].text
        grammatical_info = results.find_all("span", class_="grammatica")[0].text

        translations = [x.text for x in results.find_all("span", class_="english")]
        polish_translations = [scraper.deepl_translation_en_to_pl(x) for x in translations]

        return word, grammatical_info, polish_translations


    with open(output_temporary_file_name, 'a', encoding="utf-8") as f:
        for input_word in sys.argv[1:]:

            try:
                word, grammatical_info, polish_translations = scrape()


                def is_present(pattern) -> bool:
                    return re.search(pattern, grammatical_info) is not None


                msg = None
                if is_present(verb_pattern):
                    msg = f', {scraper.verb_forms(word)} {scraper.verb_metadata(grammatical_info)}\n'
                elif is_present(noun_pattern):
                    msg = f', {scraper.full_gen_sing(word)} {scraper.noun_metadata(grammatical_info)}\n'
                elif is_present(adverb_pattern):
                    msg = f' {scraper.adverb_metadata()}\n'
                elif is_present(preposition_pattern):
                    msg = f' {scraper.preposition_metadata()}\n'
                elif is_present(conjunction_pattern):
                    msg = f' {scraper.conjunction_metadata()}\n'
                elif is_present(adjective_pattern):
                    msg = f', {scraper.adjective_forms(input_word)} {scraper.adjective_metadata()}\n'
                else:
                    msg = f' cannot parse. printing raw instead\n{grammatical_info}\n'

                print_and_write(word)
                print_and_write(msg)
                print_and_write('()\n')

                for t, i in zip(polish_translations, range(len(polish_translations))):
                    print_and_write(f'{i + 1}. {t}\n')

                print_and_write('\n')

            except Exception as Argument:
                logging.exception(f'cannot scrape {input_word}')
                print()
