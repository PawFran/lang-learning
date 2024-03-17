from scraping.lib.latin_scraper import LatinDictScraper

scraper = LatinDictScraper(None, None, None)


def test_verb_metadata():
    assert scraper.verb_metadata('transitive and intransitive verb III conjugation ending -io') == '[verb] [III]'
    assert scraper.verb_metadata('transitive verb I conjugation') == '[verb] [I]'
    assert scraper.verb_metadata('anomalous transitive verb') == '[verb] [anomalous]'


def test_noun_metadata():
    assert scraper.noun_metadata('neutral noun II declension') == '[noun] [n] [II]'
    assert scraper.noun_metadata('masculine noun II declension') == '[noun] [m] [II]'
    assert scraper.noun_metadata('feminine noun I declension') == '[noun] [f] [I]'
    assert scraper.noun_metadata('masculin and feminine noun III declension') == '[noun] [m/f] [III]'
