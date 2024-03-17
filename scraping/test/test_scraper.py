from scraping.lib.latin_scraper import LatinDictScraper

scraper = LatinDictScraper(None, None, None)


def test_verb_metadata():
    assert scraper.verb_metadata('transitive and intransitive verb III conjugation ending -io') == '[verb] [III]'
    assert scraper.verb_metadata('transitive verb I conjugation') == '[verb] [I]'
    assert scraper.verb_metadata('anomalous transitive verb') == '[verb] [anomalous]'
