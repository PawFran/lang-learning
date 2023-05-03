import re
import sys

from scraping.lib.scraper import LatinDictScraper

if len(sys.argv) == 1:
    raise Exception('must give at least one argument (word to be found)')

output_temporary_file_name = 'scraping_out_tmp.txt'

verb_pattern = '.+ verb .+'
noun_pattern = '.+ noun .+'
adverb_pattern = 'adverb'
preposition_pattern = 'preposition'
conjunction_pattern = 'conjunction'
adjective_pattern = 'adjective'

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


with open(output_temporary_file_name, 'a') as f:
    for input_word in sys.argv[1:]:
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
                raise Exception(f'''coldn't find translation for neither {input_word} nor {new_word}''')

        word = results.find_all("span", class_="lemma")[0].text
        grammatical_info = results.find_all("span", class_="grammatica")[0].text

        translations = [x.text for x in results.find_all("span", class_="english")]
        polish_translations = [scraper.deepl_translation_en_to_pl(x) for x in translations]

        print_and_write(word)


        def is_present(pattern) -> bool:
            return re.search(pattern, grammatical_info) is not None


        if is_present(verb_pattern):
            print_and_write(f', {scraper.verb_forms(word)} {scraper.verb_metadata(grammatical_info)}\n')
        elif is_present(noun_pattern):
            print_and_write(f', {scraper.full_gen_pl(word)} {scraper.noun_metadata(grammatical_info)}\n')
        elif is_present(adverb_pattern):
            print_and_write(f' {scraper.adverb_metadata()}\n')
        elif is_present(preposition_pattern):
            print_and_write(f' {scraper.preposition_metadata()}\n')
        elif is_present(conjunction_pattern):
            print_and_write(f' {scraper.conjunction_metadata()}\n')
        elif is_present(adjective_pattern):
            print_and_write(f', {scraper.adjective_forms(input_word)} {scraper.adjective_metadata()}\n')
        else:
            print_and_write(' cannot parse. printing raw instead\n')
            print_and_write(grammatical_info + '\n')

        for t, i in zip(polish_translations, range(len(polish_translations))):
            print_and_write(f'{i + 1}. {t}\n')

        print_and_write('\n')
