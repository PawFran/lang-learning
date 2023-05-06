from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

verb_pattern = '.+ verb .+'
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
        conjugation_type = filtered[filtered.index('conjugation') - 1]
        return f'[verb] [{conjugation_type}]'

    @staticmethod
    def noun_metadata(grammatical_info) -> str:
        # todo handle different variants of 3rd declension
        split = grammatical_info.split(' ')
        filtered = [segment for segment in split if len(segment) > 0]
        genre = filtered[0][0]
        declension_type = filtered[2]

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

    def get_flexion_soup(self, word) -> BeautifulSoup:
        flexion_url = f'{self.base_flexion_URL}?lemma={word}100'  # 100 means first word in case of disambiguation
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
        div_with_infinitive = divs_with_conjugation[5]

        infinitive_core = div_with_infinitive.find_all("span", {"class": "radice"})[0].text
        infinitive_ending = div_with_infinitive.find_all("span", {"class": "desinenza"})[0].text

        return infinitive_core + infinitive_ending

    # todo test it for verbs with no supine. what will happen ? would be nice to return none
    @staticmethod
    def verb_supine(divs_with_conjugation) -> str:
        div_with_infinitive = divs_with_conjugation[5]

        supine_core = div_with_infinitive.find_all("span", {"class": "radice"})[-1].text
        supine_ending = div_with_infinitive.find_all("span", {"class": "desinenza"})[-1].text

        # accents from https://www.online-latin-dictionary.com are sometimes wrong
        return (supine_core + supine_ending).replace('atum', 'ātum')

    def verb_forms(self, word) -> str:
        flexion_soup = self.get_flexion_soup(word)
        divs_with_conjugation = flexion_soup.find_all("div", {"class": "col span_1_of_2"})

        perfect_first_sing_full = self.verb_perfect_form(divs_with_conjugation)
        infinitive = self.verb_infinitive(divs_with_conjugation)
        supine = self.verb_supine(divs_with_conjugation)

        return f'{infinitive}, {perfect_first_sing_full}, {supine}'  # todo test it when there's no supine

    def full_gen_sing(self, word) -> str:
        flexion_soup = self.get_flexion_soup(word)

        divs_with_declension = flexion_soup.find_all("div", {"class": "col span_1_of_2"})
        singular_declension = divs_with_declension[0]
        singular_cores = [x.text for x in singular_declension.find_all("span", {"class": "radice"})]
        singular_endings = [x.text for x in singular_declension.find_all("span", {"class": "desinenza"})]

        gen_sing_core = singular_cores[1]
        gen_sing_ending = singular_endings[1]

        return gen_sing_core + gen_sing_ending

    def adjective_forms(self, word) -> str:
        flexion_soup = self.get_flexion_soup(word)
        divs_with_declension = flexion_soup.find_all("div", {"class": "col span_1_of_2"})

        fem_sing_declension = divs_with_declension[2]
        neut_sing_declension = divs_with_declension[4]

        nom_sing_fem_core = fem_sing_declension.find_all("span", {"class": "radice"})[0].text
        nom_sing_fem_ending = fem_sing_declension.find_all("span", {"class": "desinenza"})[0].text

        nom_sing_neut_core = neut_sing_declension.find_all("span", {"class": "radice"})[0].text
        nom_sing_neut_ending = neut_sing_declension.find_all("span", {"class": "desinenza"})[0].text

        femininum = nom_sing_fem_core + nom_sing_fem_ending
        neutrum = nom_sing_neut_core + nom_sing_neut_ending

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
