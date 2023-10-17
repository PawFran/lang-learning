from common.lib.utils import *


def test_weak_compare():
    assert weak_equals('castīgo', 'castigo')
    assert weak_equals('castīgo', 'castigo ')
    assert weak_equals('castīgo', 'castīgo')
    assert weak_equals('castīgo', 'castīgo ')
    assert not weak_equals('castīgo', 'castīg')
    assert weak_equals('castāre', 'castare')
    assert weak_equals('valdē', 'valde')
    assert weak_equals('ăënĕus', 'aeneus')


def test_wek_compare_uppercase():
    assert weak_equals('Ī', 'ī')
    assert weak_equals('ī', 'Ī')
    assert weak_equals('Ī', 'I')
