import re
import sys
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

if len(sys.argv) == 1:
    raise Exception('must give at least one argument (word to be found)')

output_temporary_file_name = 'scraping_out_tmp.txt'


def verb_metadata(grammatical_info) -> str:
    split = grammatical_info.split(' ')
    filtered = [segment for segment in split if len(segment) > 0]
    conjugation_type = filtered[-2]
    return f'[verb] [{conjugation_type}]'


def noun_metadata(grammatical_info) -> str:
    # todo handle different variants of 3rd declension
    split = grammatical_info.split(' ')
    filtered = [segment for segment in split if len(segment) > 0]
    genre = filtered[0][0]
    declension_type = filtered[2]

    return f'[noun] [{genre}] [{declension_type}]'


def adverb_metadata() -> str:
    return '[adv]'


def preposition_metadata() -> str:
    return '[prep]'


def conjunction_metadata() -> str:
    return '[conj]'


def adjective_metadata() -> str:
    return '[adj]'


def get_flexion_soup(word) -> BeautifulSoup:
    flexion_url = f'https://www.online-latin-dictionary.com/latin-dictionary-flexion.php?lemma={word}'
    flexion_page = requests.get(flexion_url)
    flexion_soup = BeautifulSoup(flexion_page.content, "html.parser")
    return flexion_soup


def verb_perfect_form(divs_with_conjugation) -> str:
    div_with_perfect_conjugation = divs_with_conjugation[1]
    perfect_first_sing_core = div_with_perfect_conjugation.find_all("span", {"class": "radice"})[0].text
    perfect_first_sing_ending = div_with_perfect_conjugation.find_all("span", {"class": "desinenza"})[0].text

    # accents from https://www.online-latin-dictionary.com are sometimes wrong
    return (perfect_first_sing_core + perfect_first_sing_ending).replace('avi', 'āvī')


def verb_infinitive(divs_with_conjugation) -> str:
    div_with_infinitive = divs_with_conjugation[5]

    infinitive_core = div_with_infinitive.find_all("span", {"class": "radice"})[0].text
    infinitive_ending = div_with_infinitive.find_all("span", {"class": "desinenza"})[0].text

    return infinitive_core + infinitive_ending


# todo test it for verbs with no supine. what will happen ? would be nice to return none
def verb_supine(divs_with_conjugation) -> str:
    div_with_infinitive = divs_with_conjugation[5]

    supine_core = div_with_infinitive.find_all("span", {"class": "radice"})[-1].text
    supine_ending = div_with_infinitive.find_all("span", {"class": "desinenza"})[-1].text

    # accents from https://www.online-latin-dictionary.com are sometimes wrong
    return (supine_core + supine_ending).replace('atum', 'ātum')


def verb_forms(word) -> str:
    flexion_soup = get_flexion_soup(word)
    divs_with_conjugation = flexion_soup.find_all("div", {"class": "col span_1_of_2"})

    perfect_first_sing_full = verb_perfect_form(divs_with_conjugation)
    infinitive = verb_infinitive(divs_with_conjugation)
    supine = verb_supine(divs_with_conjugation)

    return f'{infinitive}, {perfect_first_sing_full}, {supine}'  # todo test it when there's no supine


def full_gen_pl(word) -> str:
    flexion_soup = get_flexion_soup(word)

    divs_with_declension = flexion_soup.find_all("div", {"class": "col span_1_of_2"})
    plural_declension = divs_with_declension[1]
    plural_cores = [x.text for x in plural_declension.find_all("span", {"class": "radice"})]
    plural_endings = [x.text for x in plural_declension.find_all("span", {"class": "desinenza"})]

    gen_pl_core = plural_cores[1]
    gen_pl_ending = plural_endings[1]

    return gen_pl_core + gen_pl_ending


def adjective_forms(word) -> str:
    flexion_soup = get_flexion_soup(word)
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


def deepl_translation_en_to_pl(en_word) -> str:
    text_encoded = quote(en_word)
    data = f'text={text_encoded}&source_lang=EN&target_lang=PL'

    response = requests.post('https://api-free.deepl.com/v2/translate', headers=deepl_headers, data=data)

    # can be more than one translation ?
    pl_translations = response.json()['translations']

    if len(pl_translations) > 1:
        raise Exception(f'unexpectedly more than one translation was returned: {en_word} -> {pl_translations}')

    return pl_translations[0]['text']


def print_and_write(text):
    print(text, end='')
    f.write(text)


verb_pattern = '.+ verb .+'
noun_pattern = '.+ noun .+'
adverb_pattern = 'adverb'
preposition_pattern = 'preposition'
conjunction_pattern = 'conjunction'
adjective_pattern = 'adjective'

base_URL = 'https://www.online-latin-dictionary.com/latin-english-dictionary.php'

deepl_headers = {
    'Authorization': 'DeepL-Auth-Key 0346e75c-3679-c5ed-4ac4-260beade18db:fx',
    'Content-Type': 'application/x-www-form-urlencoded',
}

with open(output_temporary_file_name, 'w') as f:
    for input_word in sys.argv[1:]:
        URL = base_URL + f'?parola={input_word}'

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find(id="myth")

        word = results.find_all("span", class_="lemma")[0].text
        grammatical_info = results.find_all("span", class_="grammatica")[0].text

        translations = [x.text for x in results.find_all("span", class_="english")]
        polish_translations = [deepl_translation_en_to_pl(x) for x in translations]

        print_and_write(word)


        def is_present(pattern) -> bool:
            return re.search(pattern, grammatical_info) is not None


        if is_present(verb_pattern):
            print_and_write(f', {verb_forms(input_word)} {verb_metadata(grammatical_info)}\n')
        elif is_present(noun_pattern):
            print_and_write(f', {full_gen_pl(input_word)} {noun_metadata(grammatical_info)}\n')
        elif is_present(adverb_pattern):
            print_and_write(f' {adverb_metadata()}\n')
        elif is_present(preposition_pattern):
            print_and_write(f' {preposition_metadata()}\n')
        elif is_present(conjunction_pattern):
            print_and_write(f' {conjunction_metadata()}\n')
        elif is_present(adjective_pattern):
            print_and_write(f', {adjective_forms(input_word)} {adjective_metadata()}\n')
        else:
            print_and_write(' cannot parse. printing raw instead\n')
            print_and_write(grammatical_info + '\n')

        for t, i in zip(polish_translations, range(len(polish_translations))):
            print_and_write(f'{i + 1}. {t}\n')

        print_and_write('\n')
