from urllib.parse import quote
from dataclasses import dataclass

import requests
import re
from bs4 import BeautifulSoup, Tag

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
pronoun_pattern = '.*pronoun.*'


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
    def pronoun_metadata() -> str:
        return '[pron]'

    @staticmethod
    def adjective_metadata() -> str:
        return '[adj]'

    def get_dict_html(self, input_word) -> BeautifulSoup:
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
    def find_index_of_tag_by_text(tags, txt, strict=True):
        if strict:
            for i in range(len(tags)):
                if tags[i].text == txt:
                    return i
        else:
            for i in range(len(tags)):
                current_tag = tags[i]
                if txt in current_tag.text:
                    return i
        return None

    @staticmethod
    def find_children_tags(divs, txt):
        txt_tag_index = LatinDictScraper.find_index_of_tag_by_text(divs, txt=txt)
        tag_container = divs[txt_tag_index + 1]

        return [x for x in tag_container.children if type(x) == Tag]

    @staticmethod
    def find_children_2_tags(divs, txt1, txt2):
        txt1_tag_index = LatinDictScraper.find_index_of_tag_by_text(divs, txt=txt1)
        divs_after_txt1 = divs[txt1_tag_index:]

        return LatinDictScraper.find_children_tags(divs_after_txt1, txt2)

    @staticmethod
    def verb_forms(html_with_conjugations: BeautifulSoup) -> str:
        all_divs = html_with_conjugations.find_all('div')

        perfect_children_tags = LatinDictScraper.find_children_2_tags(all_divs, txt1='INDICATIVE', txt2='PERFECT')
        perfect_form = LatinDictScraper.get_person(perfect_children_tags, person_number=0, person_name='I sing')

        infinitive_children_tags = LatinDictScraper.find_children_2_tags(all_divs, txt1='INFINITIVE', txt2='PRESENT')
        infinitive_form = infinitive_children_tags[0].text.strip()

        supine_children_tags = LatinDictScraper.find_children_tags(all_divs, txt='SUPIN')
        supine_form = supine_children_tags[0].text.strip()

        result = infinitive_form
        if perfect_form != '–':
            result += f', {perfect_form}'
        if supine_form != '–':
            result = f'{result}, {supine_form}'

        return result

    @staticmethod
    def get_person(tags: [Tag], person_number: int, person_name: str):
        person_and_value = tags[person_number].text.strip().split('.')
        person = person_and_value[0]
        value = person_and_value[1]
        if person == person_name:
            perfect_form = value
            return perfect_form
        else:
            raise Exception('cannot parse perfect form')

    @staticmethod
    def get_case(tags: [Tag], case_number: int, case_name: str) -> str:
        case_and_value = tags[case_number].text.strip().split('.')
        grammatical_case = case_and_value[0]
        value = case_and_value[1]
        if grammatical_case != case_name:
            raise Exception(f'cannot parse {case_name}')

        return value

    @staticmethod
    def nominative_from_children_tags(tags) -> str:
        return LatinDictScraper.get_case(tags, 0, 'Nom')

    @staticmethod
    def genetive_from_children_tags(tags) -> str:
        return LatinDictScraper.get_case(tags, 1, 'Gen')

    @staticmethod
    def full_gen_sing(html_with_declension: BeautifulSoup) -> str:
        all_divs = html_with_declension.find_all('div')
        children_tags = LatinDictScraper.find_children_2_tags(all_divs, txt1='MASCULINE', txt2='SINGULAR')

        return LatinDictScraper.genetive_from_children_tags(children_tags)

    @staticmethod
    def nominative(tags: [Tag], txt1: str, txt2: str):
        children_tags = LatinDictScraper.find_children_2_tags(tags, txt1, txt2)
        return LatinDictScraper.nominative_from_children_tags(children_tags)

    @staticmethod
    def adjective_forms(html_with_declension: BeautifulSoup) -> str:
        all_divs = html_with_declension.find_all('div')

        nom_sing_fem = LatinDictScraper.nominative(all_divs, 'FEMININE', 'SINGULAR')
        nom_sing_neut = LatinDictScraper.nominative(all_divs, 'NEUTER', 'SINGULAR')

        return f'{nom_sing_fem}, {nom_sing_neut}'

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
