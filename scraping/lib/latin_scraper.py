from urllib.parse import quote
from dataclasses import dataclass

import requests
import re
from bs4 import BeautifulSoup

URL_main_part = 'https://www.online-latin-dictionary.com'
base_dict_URL = f'{URL_main_part}/latin-english-dictionary.php'
base_flexion_URL = f'{URL_main_part}/latin-dictionary-flexion.php'

deepl_headers = {
    'Authorization': 'DeepL-Auth-Key 0346e75c-3679-c5ed-4ac4-260beade18db:fx',
    'Content-Type': 'application/x-www-form-urlencoded',
}

verb_pattern = '.+ verb.*'
noun_pattern = '.+ noun .+'
adverb_pattern = 'adverb'
preposition_pattern = 'preposition'
conjunction_pattern = 'conjunction'
adjective_pattern = 'adjective'


class LatinDictScraper:

    def __init__(self, base_dict_URL, base_flexion_URL, deepl_headers):
        self.base_dict_URL = base_dict_URL
        self.base_flexion_URL = base_flexion_URL
        self.deepl_headers = deepl_headers

    @staticmethod
    def verb_metadata(grammatical_info) -> str:
        split = grammatical_info.split(' ')
        filtered = [segment for segment in split if len(segment) > 0]

        # info about conjugation type is just before "conjugation" word (other words may be different)
        conjugation_type = 'anomalous' if 'anomalous' in filtered else filtered[filtered.index('conjugation') - 1]
        return f'[verb] [{conjugation_type}]'

    @staticmethod
    def noun_metadata(grammatical_info) -> str:
        # todo handle different variants of 3rd declension
        split = grammatical_info.split(' ')
        filtered = [segment for segment in split if len(segment) > 0]
        declension_type = filtered[-2]

        if re.search('masculin and feminine', grammatical_info) is not None:
            genre = 'm/f'
        else:
            genre = filtered[0][0]

        return f'[noun] [{genre}] [{declension_type}]'

    @staticmethod
    def adverb_metadata() -> str:
        return '[adv]'

    @staticmethod
    def preposition_metadata() -> str:
        return '[prep]'

    @staticmethod
    def conjunction_metadata() -> str:
        return '[conj]'

    @staticmethod
    def adjective_metadata() -> str:
        return '[adj]'

    def get_dict_soup(self, input_word) -> BeautifulSoup:
        dict_URL = self.base_dict_URL + f'?parola={input_word}'

        page = requests.get(dict_URL)
        return BeautifulSoup(page.content, "html.parser")

    @staticmethod
    def get_flexion_soup(flexion_anchor) -> BeautifulSoup:
        flexion_url = URL_main_part + flexion_anchor
        flexion_page = requests.get(flexion_url)
        flexion_soup = BeautifulSoup(flexion_page.content, "html.parser")
        return flexion_soup

    @staticmethod
    def verb_perfect_form(divs_with_conjugation) -> str:
        div_with_perfect_conjugation = divs_with_conjugation[1]
        perfect_first_sing_core = div_with_perfect_conjugation.find_all("span", {"class": "radice"})[0].text
        perfect_first_sing_ending = div_with_perfect_conjugation.find_all("span", {"class": "desinenza"})[0].text

        # accents from https://www.online-latin-dictionary.com are sometimes wrong
        return (perfect_first_sing_core + perfect_first_sing_ending).replace('avi', 'āvī')

    @staticmethod
    def verb_infinitive(divs_with_conjugation) -> str:
        div_with_infinitive_at_list = divs_with_conjugation[5].text.split('\n')
        present_infinitive_index = div_with_infinitive_at_list.index('PRESENT') + 1

        infinitive = div_with_infinitive_at_list[present_infinitive_index].strip()

        return None if infinitive == '-' else infinitive

    @staticmethod
    def verb_supine(divs_with_conjugation) -> str:
        div_with_infinitive_as_list = divs_with_conjugation[5].text.split('\n')

        supine_index = div_with_infinitive_as_list.index('SUPIN') + 1
        supine = div_with_infinitive_as_list[supine_index].strip()

        if supine == '–':
            return None
        else:
            return supine.replace('atum', 'ātum')
            # accents from https://www.online-latin-dictionary.com are sometimes wrong

    @staticmethod
    def verb_forms(flexion_soup) -> str:
        divs_with_conjugation = flexion_soup.find_all("div", {"class": "col span_1_of_2"})

        perfect_first_sing_full = LatinDictScraper.verb_perfect_form(divs_with_conjugation)
        infinitive = LatinDictScraper.verb_infinitive(divs_with_conjugation)
        supine = LatinDictScraper.verb_supine(divs_with_conjugation)

        inf_and_perfect = f'{infinitive}, {perfect_first_sing_full}'

        if supine is not None:
            return inf_and_perfect + f', {supine}'
        else:
            return inf_and_perfect

    @staticmethod
    def full_gen_sing(flexion_soup) -> str:
        divs_with_declension = flexion_soup.find_all("div", {"class": "col span_1_of_2"})
        singular_declension = divs_with_declension[0]

        result_set = singular_declension.find_all("tr")
        for tag in result_set:
            if [x for x in tag][0].contents[0] == 'Gen.':
                both = [x for x in tag][1]
                gen_sing_core = both.find_all("span", {"class": "radice"})[0].contents[0]
                gen_sing_ending = both.find_all("span", {"class": "desinenza"})[0].contents[0]

                return gen_sing_core + gen_sing_ending

        raise Exception('cannot parse Gen singularis')

    @staticmethod
    def adjective_form(declension):
        fem_result_set = declension.find_all('tr')

        for tag in fem_result_set:
            if [x for x in tag][0].contents[0] == 'Nom.':
                core = tag.find_all("span", {"class": "radice"})[0].contents[0]
                ending = ''  # ex ferox
                try:
                    ending = tag.find_all("span", {"class": "desinenza"})[0].contents[0]
                except IndexError:
                    pass

                return core + ending

        return None

    @staticmethod
    def adjective_forms(flexion_soup) -> str:
        divs_with_declension = flexion_soup.find_all("div", {"class": "col span_1_of_2"})

        fem_sing_declension = divs_with_declension[2]
        neut_sing_declension = divs_with_declension[4]

        femininum = LatinDictScraper.adjective_form(fem_sing_declension)
        neutrum = LatinDictScraper.adjective_form(neut_sing_declension)

        if femininum is None or neutrum is None:
            raise Exception(f'cannot find femininum or neutrum forms for this adjective')  # todo do sth with it

        return f'{femininum}, {neutrum}'

    def deepl_translation_en_to_pl(self, en_word) -> str:
        text_encoded = quote(en_word)
        data = f'text={text_encoded}&source_lang=EN&target_lang=PL'

        response = requests.post('https://api-free.deepl.com/v2/translate', headers=self.deepl_headers, data=data)

        # can be more than one translation ?
        pl_translations = response.json()['translations']

        if len(pl_translations) > 1:
            raise Exception(f'unexpectedly more than one translation was returned: {en_word} -> {pl_translations}')

        return pl_translations[0]['text']


@dataclass
class LatinScrapeResults:
    word: str
    grammatical_info: str
    polish_translations: [str]
