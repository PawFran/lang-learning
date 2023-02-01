from lib.utils import *


def test_weak_compare():
    assert weak_compare('castīgo', 'castigo')
    assert weak_compare('castīgo', 'castigo ')
    assert weak_compare('castīgo', 'castīgo')
    assert weak_compare('castīgo', 'castīgo ')
    assert not weak_compare('castīgo', 'castīg')
    assert weak_compare('castāre', 'castare')
    assert weak_compare('valdē', 'valde')