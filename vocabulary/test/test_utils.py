from vocabulary.lib.utils import *


def test_weak_compare():
    assert weak_compare('castīgo', 'castigo')
    assert weak_compare('castīgo', 'castigo ')
    assert weak_compare('castīgo', 'castīgo')
    assert weak_compare('castīgo', 'castīgo ')
    assert not weak_compare('castīgo', 'castīg')
    assert weak_compare('castāre', 'castare')
    assert weak_compare('valdē', 'valde')


def test_wek_compare_uppercase():
    assert weak_compare('Ī', 'ī')
    assert weak_compare('ī', 'Ī')
    assert weak_compare('Ī', 'I')


conjugation_pattern = '\[I{1,3}V*\]'
genre_pattern = '\[[fmn]\]'


def test_extract_from_square_brackets():
    assert extract_from_square_brackets(conjugation_pattern, 'specto, āre, avi, atum [verb] [I]') == 'I'
    assert extract_from_square_brackets(genre_pattern, 'vinea, ae [noun] [I] [f]') == 'f'
