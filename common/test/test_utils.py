from common.lib.utils import special_replaced, weak_equals, weak_in, flatten


def test_replace_special():
    assert special_replaced('pūniō') == 'punio'
    assert special_replaced('ēnarro') == 'enarro'
    assert special_replaced('complūres') == 'complures'
    assert special_replaced('sēnsim') == 'sensim'



def test_weak_in():
    latin_words = ['pūniō', 'castīgō', 'neco']

    assert weak_in('punio', latin_words)
    assert weak_in('punio ', latin_words)
    assert weak_in('CASTIGO', latin_words)

    assert not weak_in('interficio', latin_words)
    assert not weak_in('CASTIGO', latin_words, case_sensitive=True)


def test_flatten():
    nested_list = [['pūniō', 'castīgō'], ['neco', 'interficio']]
    assert flatten(nested_list) == ['pūniō', 'castīgō', 'neco', 'interficio']


def test_weak_compare():
    # equals
    assert weak_equals('castīgo', 'castigo')  # macron
    assert weak_equals('castīgo', 'castigo ')  # space
    assert weak_equals('castīgo', 'castīgo')  # same

    assert weak_equals('ăënĕus', 'aeneus')  # breve + diaeresis

    assert weak_equals('complūres', 'COMPLURES')  # case
    assert weak_equals('complūres', 'COMPLURES', case_sensitive=False)  # case + explicit arg
    assert weak_equals('sēnsim', 'sensim', case_sensitive=True)  # explicit arg

    # not equals
    assert not weak_equals('complūres', 'COMPLURES', case_sensitive=True)  # case
    assert not weak_equals('castīgo', 'castīg')
    assert not weak_equals('pūniō', 'punioo')
