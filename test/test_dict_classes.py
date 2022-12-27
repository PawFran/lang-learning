from lib.parsing_dict import *


def test_conjugation():
    assert Verb.which_conjugation('castīgo, āre, avi, atum [verb] [I]') == 'I'
    assert Verb.which_conjugation('maneō, ēre, sī, sum [verb] [II]') == 'II'
    assert Verb.which_conjugation('ostendō, ere, dī, tum(sum) [verb] [III]') == 'III'
    # add IIIa ?
    assert Verb.which_conjugation('sentiō, īre, sī, sum [verb] [IV]') == 'IV'


def test_declension():
    assert Noun.which_declension('cōpia, ae [noun] [I] [f]') == 'I'
    assert Noun.which_declension('exiguum, ī [noun] [II] [n]') == 'II'
    assert Noun.which_declension('omnia, ium [noun] [III vowel] [n] [pl]') == 'III vowel'
    assert Noun.which_declension('hospes, itis [noun] [III consonant] [m]') == 'III consonant'
    assert Noun.which_declension('turris, is [noun] [III mixed] [f]') == 'III mixed'
    assert Noun.which_declension('equitātus, ūs [noun] [IV] [m]') == 'IV'
    assert Noun.which_declension('saniēs, ēī [noun] [V] [f]') == 'V'


def test_is_verb():
    assert Verb.is_verb('castīgo, āre, avi, atum [verb] [I]')
    assert not Verb.is_verb('vinea, ae [noun] [I] [f]')


def test_verb_from_entry_head():
    line = 'castīgo, āre, avi, atum [verb] [I]'
    verb = Verb.from_entry_head(line)
    assert verb.base == 'castīgo'
    assert verb.head_raw == line
    assert verb.infinite == 'āre'
    assert verb.perfect == 'avi'
    assert verb.supine == 'atum'
    assert verb.conjugation == 'I'
    # todo handle and test case when not all forms are given


def test_is_noun():
    assert not Noun.is_noun('castīgo, āre, avi, atum [verb] [I]')
    assert Noun.is_noun('vinea, ae [noun] [I] [f]')


def test_which_genre():
    assert Noun.which_genre('vinea, ae [noun] [I] [f]') == 'f'
    # todo add other examples


def test_only_plural():
    assert Noun.is_only_plural('multae, ārum [noun] [I] [pl]')
    assert not Noun.is_only_plural('vinea, ae [noun] [I] [f]')


def test_noun_from_entry_head():
    line = 'vinea, ae [noun] [I] [f]'
    noun = Noun.from_entry_head(line)
    assert noun.base == 'vinea'
    assert noun.head_raw == line
    assert noun.genetive == 'ae'
    assert noun.genre == 'f'
    assert not noun.only_plural
    assert noun.declension == 'I'
    # todo add onl plural noun


def test_is_adverb():
    assert Adverb.is_adverb('saepe [adv]')
    assert not Adverb.is_adverb('vinea, ae [noun] [I] [f]')


def test_adverb_from_entry_head():
    line = 'saepe [adv]'
    adverb = Adverb.from_entry_head(line)
    assert adverb.base == 'saepe'
    assert adverb.head_raw == line


def test_is_adjective():
    assert Adjective.is_adjective('sempiternus, a, um [adj]')
    assert not Adjective.is_adjective('saepe [adv]')


def test_adjective_from_entry_head():
    line = 'sempiternus, a, um [adj]'
    adjective = Adjective.from_entry_head(line)
    assert adjective.base == 'sempiternus'
    assert adjective.head_raw == line
    assert adjective.femininum == 'a'
    assert adjective.neutrum == 'um'
