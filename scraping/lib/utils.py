import re

from scraping.lib.latin_scraper import *


def print_and_write(f, text):
    print(text, end='')
    f.write(text)


def single_scraping_result(scraper, single_result) -> LatinScrapeResults:
    word = single_result.find_all("span", class_="lemma")[0].text
    grammatical_info = single_result.find_all("span", class_="grammatica")[0].text

    translations = [x.text for x in single_result.find_all("span", class_="english")]
    polish_translations = [scraper.deepl_translation_en_to_pl(x) for x in translations]

    return LatinScrapeResults(word, grammatical_info, polish_translations)


def scrape(scraper, input_word) -> [LatinScrapeResults]:
    soup = scraper.get_dict_soup(input_word)

    disambiguation_tags = soup.findAll('ul', {"class": "disambigua"})
    disambiguation: bool = len(disambiguation_tags) > 0
    multiple_links = len(soup.findAll('a', href=True, text=input_word)) > 1

    final_result = []

    if disambiguation:
        # process word "IN THIS PAGE"
        single_result = soup.find(id="myth")
        final_result.append(single_scraping_result(scraper, single_result))

        # process the rest
        all_anchors = disambiguation_tags[0].findAll('a', href=True)
        hrefs = [x['href'] for x in all_anchors if x['href'] != '#']

        soups = []
        for href in hrefs:
            link = URL_main_part + '/' + href
            page = requests.get(link)
            soups.append(BeautifulSoup(page.content, "html.parser"))

        for soup in soups:
            single_result = soup.find(id="myth")
            final_result.append(single_scraping_result(scraper, single_result))
    elif soup.find(id="myth") is not None:
        single_result = soup.find(id="myth")
        final_result.append(single_scraping_result(scraper, single_result))
    else:
        hrefs = []
        all_tables = [t for t in soup.findAll('table') if t.findAll('a', href=True) is not None]
        for t in all_tables:
            relevant_hrefs = [x['href'] for x in t.findAll('a', href=True) if
                                x['href'].startswith('latin-english-dictionary.php?lemma=')]
            hrefs += relevant_hrefs

        unique_hrefs = set(hrefs)
        soups = []
        for href in unique_hrefs:
            link = URL_main_part + '/' + href
            page = requests.get(link)
            soups.append(BeautifulSoup(page.content, "html.parser"))

        for soup in soups:
            single_result = soup.find(id="myth")
            final_result.append(single_scraping_result(scraper, single_result))

    if len(final_result) > 0:
        return final_result
    else:
        raise Exception(f'cannot parse {input_word}')


def parse_msg(scraper, input_word, word, grammatical_info):
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

    return msg


def print_output(f, scraper, input_word, scrape_result):
    word, grammatical_info, polish_translations = scrape_result.word, scrape_result.grammatical_info, \
        scrape_result.polish_translations

    msg = parse_msg(scraper, input_word, word, grammatical_info)

    print_and_write(f, word)
    print_and_write(f, msg)
    print_and_write(f, '()\n')

    for t, i in zip(polish_translations, range(len(polish_translations))):
        print_and_write(f, f'{i + 1}. {t}\n')

    print_and_write(f, '\n')
