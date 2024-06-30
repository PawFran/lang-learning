import os

from bs4 import BeautifulSoup

from scraping.lib.latin_scraper import LatinDictScraper
from scraping.lib.latin_scraper import verb_pattern
from scraping.lib.utils import is_present


def prepare_bs(file_name: str) -> BeautifulSoup:
    path = os.path.join('resources', file_name)
    with open(path, encoding='utf-8') as f:
        bs = BeautifulSoup(f.read())

    return bs


volo_html_with_conjugations = prepare_bs('volo_verb_example.html')
volo_html_with_declensions = prepare_bs('volo_noun_example.html')
summus_html_with_declensions = prepare_bs('summus_adj_example.html')
ferox_html_with_declensions = prepare_bs('ferox_adj_example.html')


def test_is_present_verb_pattern():
    assert is_present(verb_pattern, text='transitive and intransitive verb III conjugation ending -io')
    assert is_present(verb_pattern, text='transitive verb I conjugation')
    assert is_present(verb_pattern, text='anomalous transitive verb')

    assert not is_present(verb_pattern, text='masculine noun III declension')


def test_verb_forms():
    assert (LatinDictScraper.verb_forms(volo_html_with_conjugations) == 'velle, volui')


def test_full_gen_sing():
    assert (LatinDictScraper.full_gen_sing(volo_html_with_declensions) == 'volonis')


def test_adjective_forms():
    assert (LatinDictScraper.adjective_forms(summus_html_with_declensions) == 'summă, summum')
    assert (LatinDictScraper.adjective_forms(ferox_html_with_declensions) == 'fĕrox, fĕrox')
