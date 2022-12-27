from lib.parsing_dict import *


def test_conjugation():
    assert LatinVerb.which_conjugation('castīgo, āre, avi, atum [verb] [I]') == 'I'
    assert LatinVerb.which_conjugation('maneō, ēre, sī, sum [verb] [II]') == 'II'
    assert LatinVerb.which_conjugation('ostendō, ere, dī, tum(sum) [verb] [III]') == 'III'
    # add IIIa ?
    assert LatinVerb.which_conjugation('sentiō, īre, sī, sum [verb] [IV]') == 'IV'


def test_declension():
    assert LatinNoun.which_declension('cōpia, ae [noun] [I] [f]') == 'I'
    assert LatinNoun.which_declension('exiguum, ī [noun] [II] [n]') == 'II'
    assert LatinNoun.which_declension('omnia, ium [noun] [III vowel] [n] [pl]') == 'III vowel'
    assert LatinNoun.which_declension('hospes, itis [noun] [III consonant] [m]') == 'III consonant'
    assert LatinNoun.which_declension('turris, is [noun] [III mixed] [f]') == 'III mixed'
    assert LatinNoun.which_declension('equitātus, ūs [noun] [IV] [m]') == 'IV'
    assert LatinNoun.which_declension('saniēs, ēī [noun] [V] [f]') == 'V'


def test_is_verb():
    assert LatinVerb.is_verb('castīgo, āre, avi, atum [verb] [I]')
    assert not LatinVerb.is_verb('vinea, ae [noun] [I] [f]')


def test_verb_from_entry_head():
    line = 'castīgo, āre, avi, atum [verb] [I]'
    verb = LatinVerb.from_entry_head(line)
    assert verb.base == 'castīgo'
    assert verb.head_raw == line
    assert verb.infinite == 'āre'
    assert verb.perfect == 'avi'
    assert verb.supine == 'atum'
    assert verb.conjugation == 'I'
    # todo handle and test case when not all forms are given


def test_is_noun():
    assert not LatinNoun.is_noun('castīgo, āre, avi, atum [verb] [I]')
    assert LatinNoun.is_noun('vinea, ae [noun] [I] [f]')


def test_which_genre():
    assert LatinNoun.which_genre('vinea, ae [noun] [I] [f]') == 'f'
    # todo add other examples


def test_only_plural():
    assert LatinNoun.is_only_plural('multae, ārum [noun] [I] [pl]')
    assert not LatinNoun.is_only_plural('vinea, ae [noun] [I] [f]')


def test_noun_from_entry_head():
    line = 'vinea, ae [noun] [I] [f]'
    noun = LatinNoun.from_entry_head(line)
    assert noun.base == 'vinea'
    assert noun.head_raw == line
    assert noun.genetive == 'ae'
    assert noun.genre == 'f'
    assert not noun.only_plural
    assert noun.declension == 'I'
    # todo add onl plural noun


def test_is_adverb():
    assert LatinAdverb.is_adverb('saepe [adv]')
    assert not LatinAdverb.is_adverb('vinea, ae [noun] [I] [f]')


def test_adverb_from_entry_head():
    line = 'saepe [adv]'
    adverb = LatinAdverb.from_entry_head(line)
    assert adverb.base == 'saepe'
    assert adverb.head_raw == line


def test_is_adjective():
    assert LatinAdjective.is_adjective('sempiternus, a, um [adj]')
    assert not LatinAdjective.is_adjective('saepe [adv]')


def test_adjective_from_entry_head():
    line = 'sempiternus, a, um [adj]'
    adjective = LatinAdjective.from_entry_head(line)
    assert adjective.base == 'sempiternus'
    assert adjective.head_raw == line
    assert adjective.femininum == 'a'
    assert adjective.neutrum == 'um'


def test_english_word_which_part_of_speech():
    assert EnglishWord.which_part_of_speech('impel [verb]') == 'verb'
    assert EnglishWord.which_part_of_speech('a touch of [idiom]') == 'idiom'
    assert EnglishWord.which_part_of_speech('fancy [adj]') == 'adj'
    assert EnglishWord.which_part_of_speech('conscientiously [adv]') == 'adv'
    assert EnglishWord.which_part_of_speech('strain [noun]') == 'noun'
    assert EnglishWord.which_part_of_speech('prop something up [phrasal verb]') == 'phrasal verb'


def test_english_word_from_entry_head():
    line = 'impel [verb]'
    assert EnglishWord.from_entry_head(line) == EnglishWord(
        base='impel',
        head_raw=line,
        part_of_speech='verb'
    )

    line2 = 'a touch of [idiom]'
    assert EnglishWord.from_entry_head(line2) == EnglishWord(
        base='a touch of',
        head_raw=line2,
        part_of_speech='idiom'
    )


def test_dictionary_append():
    word = LatinAdverb(base='saepe', head_raw='saepe [adv]')
    dict_entry = DictionaryEntry(
        head=word,
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )
    dictionary = Dictionary(list())

    assert len(dictionary.entries) == 0
    dictionary.append(dict_entry)
    assert len(dictionary.entries) == 1
