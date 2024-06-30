import re
import logging

from scraping.lib.latin_scraper import *
from vocabulary.lib.dict_classes import DictionaryEntry, LatinVerb, LatinNoun, LatinAdverb, LatinPreposition, \
    LatinConjunction, LatinAdjective

output_temporary_file_name = 'scraping_out_tmp.txt'


def print_and_write(f, text):
    print(text)
    f.write(text + '\n')


def is_present(pattern, text) -> bool:
    return re.search(pattern, text) is not None


def single_scraping_result(scraper, single_result) -> LatinScrapeResults:
    word = single_result.find_all("span", class_="lemma")[0].text
    grammatical_info = single_result.find_all("span", class_="grammatica")[0].text

    translations = [x.text for x in single_result.find_all("span", class_="english")]
    polish_translations = [scraper.deepl_translation_en_to_pl(x) for x in translations]

    return LatinScrapeResults(word, grammatical_info, polish_translations)


def dict_entry_from_soup(scraper, dict_soup) -> DictionaryEntry:
    single_result = dict_soup.find(id="myth")
    summary_and_translations: LatinScrapeResults = single_scraping_result(scraper, single_result)

    this_href = single_result.findAll('a', href=True)[0]['href']
    flexion_soup = LatinDictScraper.get_flexion_soup(this_href)

    return parse_dict_entry(flexion_soup, summary_and_translations)


def scrape(scraper, input_word) -> [DictionaryEntry]:
    dict_soup = scraper.get_dict_soup(input_word)

    disambiguation_tags = dict_soup.findAll('ul', {"class": "disambigua"})
    disambiguation: bool = len(disambiguation_tags) > 0

    final_result: [DictionaryEntry] = []

    if disambiguation:
        # process word "IN THIS PAGE"
        parsed = dict_entry_from_soup(scraper, dict_soup)
        final_result.append(parsed)

        # process the rest
        all_other_anchors = disambiguation_tags[0].findAll('a', href=True)
        all_other_hrefs = [x['href'] for x in all_other_anchors if x['href'] != '#']

        all_other_soups = []
        for href in all_other_hrefs:
            link = URL_main_part + '/' + href
            page = requests.get(link)
            all_other_soups.append(BeautifulSoup(page.content, "html.parser"))

        for soup in all_other_soups:
            parsed = dict_entry_from_soup(scraper, soup)
            final_result.append(parsed)
    elif dict_soup.find(id="myth") is not None:
        parsed = dict_entry_from_soup(scraper, dict_soup)
        final_result.append(parsed)
    else:
        container_with_hrefs = dict_soup.find_all('div', {'class': 'ff_search_container pb-2'})[0]
        unique_hrefs = {x['href'] for x in container_with_hrefs.find_all('a', href=True)}

        all_other_soups = []
        for link in unique_hrefs:
            page = requests.get(link)
            all_other_soups.append(BeautifulSoup(page.content, "html.parser"))

        for dict_soup in all_other_soups:
            parsed = dict_entry_from_soup(scraper, dict_soup)
            final_result.append(parsed)

    if len(final_result) > 0:
        return final_result
    else:
        raise Exception(f'cannot parse {input_word}')


def parse_dict_entry(flexion_soup, summary_and_translations) -> DictionaryEntry:
    grammatical_info = summary_and_translations.grammatical_info
    word = summary_and_translations.word
    translations = summary_and_translations.polish_translations

    if is_present(verb_pattern, grammatical_info):
        msg = f', {LatinDictScraper.verb_forms(flexion_soup)} {LatinDictScraper.verb_metadata(grammatical_info)}'
        header = LatinVerb.from_entry_head(word + msg)
    elif is_present(noun_pattern, grammatical_info):
        msg = f', {LatinDictScraper.full_gen_sing(flexion_soup)} {LatinDictScraper.noun_metadata(grammatical_info)}'
        header = LatinNoun.from_entry_head(word + msg)
    elif is_present(adverb_pattern, grammatical_info):
        msg = f' {LatinDictScraper.adverb_metadata()}'
        header = LatinAdverb.from_entry_head(word + msg)
    elif is_present(preposition_pattern, grammatical_info):
        msg = f' {LatinDictScraper.preposition_metadata()}'
        header = LatinPreposition.from_entry_head(word + msg)
    elif is_present(conjunction_pattern, grammatical_info):
        msg = f' {LatinDictScraper.conjunction_metadata()}'
        header = LatinConjunction.from_entry_head(word + msg)
    elif is_present(adjective_pattern, grammatical_info):
        msg = f', {LatinDictScraper.adjective_forms(flexion_soup)} {LatinDictScraper.adjective_metadata()}'
        header = LatinAdjective.from_entry_head(word + msg)
    else:
        raise Exception(f'cannot parse')

    entry = DictionaryEntry(head=header, example='', translations=translations)

    return entry


def print_and_write_to_file(f, dict_entry: DictionaryEntry):
    print_and_write(f, dict_entry.head.head_raw)
    print_and_write(f, '()')

    translations = dict_entry.translations
    for t, i in zip(translations, range(len(translations))):
        print_and_write(f, f'{i + 1}. {t}')

    print_and_write(f, '')


def print_scraping_results(f, results):
    for scrape_result in results:
        print_and_write_to_file(f, scrape_result)


# this method is meant to be used from find_or_scrape_latin.py
def get_scraped_data(words_to_be_found) -> [DictionaryEntry]:
    scraper = LatinDictScraper(base_dict_URL, base_flexion_URL, deepl_headers)

    aggregated_results: [DictionaryEntry] = []

    for word in words_to_be_found:

        try:
            scrape_results: [DictionaryEntry] = scrape(scraper, word)
            aggregated_results += scrape_results

        except Exception as Argument:
            print(f'\ncannot scrape {word}')
            # logging.exception(f'cannot scrape {word}')
            print()

    return aggregated_results
