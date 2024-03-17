from scraping.lib.utils import is_present
from scraping.lib.latin_scraper import verb_pattern


def test_is_present_verb_pattern():
    assert is_present(verb_pattern, text='transitive and intransitive verb III conjugation ending -io')
    assert is_present(verb_pattern, text='transitive verb I conjugation')
    assert is_present(verb_pattern, text='anomalous transitive verb')

    assert not is_present(verb_pattern, text='masculine noun III declension')
