from datetime import timedelta

import pytest

import vocabulary.lib.db
from vocabulary.lib.dict_classes import *


def test_extract_from_square_brackets():
    conjugation_pattern = '\[I{1,3}V*\]'
    genre_pattern = '\[[fmn]\]'

    assert AbstractWord.extract_from_square_brackets(conjugation_pattern, 'specto, āre, avi, atum [verb] [I]') == 'I'
    assert AbstractWord.extract_from_square_brackets(genre_pattern, 'vinea, ae [noun] [I] [f]') == 'f'


def test_extract_metadata():
    assert AbstractWord.extract_metadata('ĭnĭmīcus, i [noun] [m] [II]') == ['noun', 'm', 'II']
    assert AbstractWord.extract_metadata('copiae, ārum [noun] [f] [I] [pl]') == ['noun', 'f', 'I', 'pl']
    assert AbstractWord.extract_metadata('mŏnĕo, mŏnēre, monui, monitum [verb] [II]') == ['verb', 'II']
    assert AbstractWord.extract_metadata('dīlĭgentĕr [adv]') == ['adv']


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


def test_verb_from_entry_head_partial():
    line = 'sum, esse, fuī [verb]'
    verb = LatinVerb.from_entry_head(line)
    assert verb.base == 'sum'
    assert verb.head_raw == line
    assert verb.infinite == 'esse'
    assert verb.perfect == 'fuī'
    assert verb.supine is None
    assert verb.conjugation is None


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


def test_is_preposition():
    assert LatinPreposition.is_preposition('in [prep]')
    assert not LatinPreposition.is_preposition('vinea, ae [noun] [I] [f]')


def test_preposition_from_entry_head():
    line = 'in [prep]'
    adverb = LatinPreposition.from_entry_head(line)
    assert adverb.base == 'in'
    assert adverb.head_raw == line


def test_is_conjunction():
    assert LatinConjunction.is_conjunction('etiam [conj]')
    assert not LatinConjunction.is_conjunction('vinea, ae [noun] [I] [f]')


def test_conjunction_from_entry_head():
    line = 'etiam [conj]'
    conjunction = LatinConjunction.from_entry_head(line)
    assert conjunction.base == 'etiam'
    assert conjunction.head_raw == line


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

    line3 = 'prop something up [phrasal verb]'
    assert EnglishWord.from_entry_head(line3) == EnglishWord(
        base='prop something up',
        head_raw=line3,
        part_of_speech='phrasal verb'
    )


def test_dictionary_append():
    word = LatinAdverb(base='saepe', head_raw='saepe [adv]')
    dict_entry = DictionaryEntry(
        head=word,
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )
    dictionary = Dictionary(list(), lang='latin')

    assert dictionary.length() == 0
    dictionary.append(dict_entry)
    assert dictionary.length() == 1


def test_dictionary_remove_entry():
    word = LatinAdverb(base='saepe', head_raw='saepe [adv]')
    dict_entry = DictionaryEntry(
        head=word,
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )
    dictionary = Dictionary([dict_entry], lang='latin')
    assert dictionary.length() == 1
    dictionary.remove_entry(dict_entry)
    assert dictionary.length() == 0


def test_dictionary_remove_single_translation():
    word = LatinPreposition(base='in', head_raw='in [prep]')
    dict_entry = DictionaryEntry(
        head=word,
        example='In Polonia habitamus',
        translations=['do (+ acc)', 'w (+ abl)']
    )

    dictionary = Dictionary([dict_entry], lang='latin')
    assert dictionary.length() == 1

    dictionary.remove_single_translation(dict_entry, 'do (+ acc)')
    assert dictionary.length() == 1
    assert dictionary.entries[0].translations == ['w (+ abl)']

    dictionary.remove_single_translation(dict_entry, 'do (+ acc)')
    assert dictionary.length() == 0


def test_weak_index():
    dict_entry1 = DictionaryEntry(
        head=LatinAdverb(base='saepe', head_raw='saepe [adv]'),
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )

    dict_entry2 = DictionaryEntry(
        head=LatinAdverb(base='valdē', head_raw='valdē [adv]'),
        example='Varsoviam valde amamus',
        translations=['bardzo']
    )

    dictionary = Dictionary(entries=[dict_entry1, dict_entry2], lang='latin')

    assert dictionary.weak_index('saepe') == 0
    assert dictionary.weak_index('valdē') == 1
    assert dictionary.weak_index('valde') == 1
    assert dictionary.weak_index('impel') is None


def test_find_by_header_using_weak_compare():
    dict_entry1 = DictionaryEntry(
        head=LatinVerb.from_entry_head('castīgo, castīgāre, castīgāvi, castīgātum [verb] [I]'),
        example='(Ancillam miseram domina sevēra castīgat)',
        translations=['karać']
    )

    dict_entry2 = DictionaryEntry(
        head=LatinAdverb(base='valdē', head_raw='valdē [adv]'),
        example='Varsoviam valde amamus',
        translations=['bardzo']
    )

    dictionary = Dictionary(entries=[dict_entry1, dict_entry2], lang='latin')

    results1 = dictionary.find_by_header_using_weak_compare('castigo ')
    results2 = dictionary.find_by_header_using_weak_compare('castigare')
    results3 = dictionary.find_by_header_using_weak_compare('asti')
    results4 = dictionary.find_by_header_using_weak_compare('valde')
    results5 = dictionary.find_by_header_using_weak_compare('verb')
    results6 = dictionary.find_by_header_using_weak_compare('I')
    results7 = dictionary.find_by_header_using_weak_compare('[')

    assert results1 == [dict_entry1]
    assert results2 == [dict_entry1]
    assert len(results3) == 0
    assert results4 == [dict_entry2]
    assert len(results5) == 0
    assert len(results6) == 0
    assert len(results7) == 0


def test_find_by_base_word_and_translation():
    dict_entry_1 = DictionaryEntry(
        head=LatinPreposition(base='in', head_raw='in [prep]'),
        example='In Polonia habitamus',
        translations=['do (+ acc)', 'pomiędzy, wśród (+ acc)', 'w (+ abl)']
    )

    dict_entry_2 = DictionaryEntry(
        head=LatinAdverb(base='saepe', head_raw='saepe [adv]'),
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )

    dictionary = Dictionary([dict_entry_1, dict_entry_2], lang='latin')

    found_1 = dictionary.find_by_base_word_and_translation(base='in', word_pl='do (+ acc)')
    found_2 = dictionary.find_by_base_word_and_translation(base='in', word_pl='pomiędzy, wśród (+ acc)')
    found_3 = dictionary.find_by_base_word_and_translation(base='saepe', word_pl='często')

    assert found_1.entry == dict_entry_1
    assert found_1.translation == 'do (+ acc)'

    assert found_2.entry == dict_entry_1
    assert found_2.translation == 'pomiędzy, wśród (+ acc)'

    assert found_3.entry == dict_entry_2
    assert found_3.translation == 'często'

    with pytest.raises(Exception):
        dictionary.find_by_base_word_and_translation(base='in', word_pl='często')


def test_weights_for_probabilities():
    assert (Dictionary.weights_for_probabilities(arr_length=5, modifier=0.5) == np.array([1, 2.5, 4.5, 7, 10])).all()


def test_word_distribution():
    dict_entry_1 = DictionaryEntry(
        head=LatinPreposition(base='in', head_raw='in [prep]'),
        example='In Polonia habitamus',
        translations=['do (+ acc)', 'pomiędzy, wśród (+ acc)', 'w (+ abl)']
    )

    dict_entry_2 = DictionaryEntry(
        head=LatinAdverb(base='saepe', head_raw='saepe [adv]'),
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )

    dict_entry_3 = DictionaryEntry(
        head=LatinAdverb(base='valdē', head_raw='valdē [adv]'),
        example='Varsoviam valde amamus',
        translations=['bardzo']
    )

    dict_entry_4 = DictionaryEntry(
        head=LatinConjunction(base='enim', head_raw='enim [conj]'),
        example='Filii agricolae in horto laborabant, agricola enim unum aut duos tantum servos habebat',
        translations=['bowiem']
    )

    dictionary = Dictionary([dict_entry_1, dict_entry_2, dict_entry_3, dict_entry_4], lang='latin')

    t1 = dt.strptime('2020-01-01 12:30:00', vocabulary.lib.db.datetime_format)

    db = pd.DataFrame({
        'word_pl': ['do (+ acc)', 'do (+ acc)', 'bardzo', 'często', 'pomiędzy, wśród (+ acc)', 'bardzo', 'do (+ acc)',
                    'do (+ acc)'],
        'translation': ['in', 'in', 'valdē', 'saepe', 'in', 'valdē', 'in', 'in'],
        'correct': [True, False, False, False, True, False, False, True],
        'time': [t1 - timedelta(minutes=int(x)) for x in np.arange(8)]
    })

    def t(mins: int):
        return str(t1 - timedelta(minutes=mins))

    to_be = pd.DataFrame({
        'word_pl': ['bowiem', 'w (+ abl)', 'często', 'bardzo', 'do (+ acc)', 'pomiędzy, wśród (+ acc)'],
        'translation': ['enim', 'in', 'saepe', 'valdē', 'in', 'in'],
        'correct_ratio_last_3_times': [np.nan, np.nan, 0, 0, 1 / 3, 1],
        'last_time': [None, None, t(3), t(2), t(0), t(4)],
        'probabilities': [(13.5 + 10) / 38.5 / 2, (13.5 + 10) / 38.5 / 2, 7 / 38.5, 4.5 / 38.5, 2.5 / 38.5, 1 / 38.5]
        # more sophisticated method for calculating probabilities is used (see test_weights_for_probabilities)
    })

    res = dictionary.words_with_distribution(db, n_last_times=3)

    assert (to_be[['word_pl', 'translation']] == res[['word_pl', 'translation']]).all().all()

    assert (to_be.probabilities - res.probabilities).sum() < 0.0001

    assert (to_be.iloc[2:, :] == res.iloc[2:, :]).all().all()

    # None and math.nan has to be compared differently
    assert res.iloc[:2, :].correct_ratio_last_3_times.isnull().all()
    assert res.iloc[:2, :].last_time.isnull().all()


def test_filter_by_simple_condition():
    dict_entry_1 = DictionaryEntry(
        head=LatinAdverb(base='saepe', head_raw='saepe [adv]'),
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )

    dict_entry_2 = DictionaryEntry(
        head=LatinAdverb(base='valdē', head_raw='valdē [adv]'),
        example='Varsoviam valde amamus',
        translations=['bardzo']
    )

    dict_entry_3 = DictionaryEntry(
        head=LatinVerb.from_entry_head('castīgo, castīgāre, castīgāvi, castīgātum [verb] [I]'),
        example='(Ancillam miseram domina sevēra castīgat)',
        translations=['karać']
    )

    dict_entry_4 = DictionaryEntry(
        head=LatinVerb.from_entry_head('colo, colere, colui, cultum[verb][III]'),
        example='(Agricolae antīqui multos deos colēbant)',
        translations=['uprawiać', 'czcić']
    )

    dictionary = Dictionary([dict_entry_1, dict_entry_2, dict_entry_3, dict_entry_4], lang='latin')

    assert dictionary.filter_by_simple_condition(['adv']).entries == [dict_entry_1, dict_entry_2]
    assert dictionary.filter_by_simple_condition(['verb', 'I']).entries == [dict_entry_3]
    assert dictionary.filter_by_simple_condition(['verb', 'IV']).entries == []
    assert dictionary.filter_by_simple_condition(['verb', 'III']).entries == [dict_entry_4]
    assert dictionary.filter_by_simple_condition(['verb']).entries == [dict_entry_3, dict_entry_4]


def test_filter_by_complex_condition():
    dict_entry_1 = DictionaryEntry(
        head=LatinAdverb(base='saepe', head_raw='saepe [adv]'),
        example='De Varsoviā poetae saepe narrant',
        translations=['często']
    )

    dict_entry_2 = DictionaryEntry(
        head=LatinAdverb(base='valdē', head_raw='valdē [adv]'),
        example='Varsoviam valde amamus',
        translations=['bardzo']
    )

    dict_entry_3 = DictionaryEntry(
        head=LatinVerb.from_entry_head('castīgo, castīgāre, castīgāvi, castīgātum [verb] [I]'),
        example='(Ancillam miseram domina sevēra castīgat)',
        translations=['karać']
    )

    dict_entry_4 = DictionaryEntry(
        head=LatinVerb.from_entry_head('colo, colere, colui, cultum[verb][III]'),
        example='(Agricolae antīqui multos deos colēbant)',
        translations=['uprawiać', 'czcić']
    )

    dict_entry_5 = DictionaryEntry(
        head=LatinNoun.from_entry_head('cūra, cūrae [noun] [f] [I]'),
        example='(Divitia tamen magnas curas et magna pericula nautis praebēbant)',
        translations=['troska']
    )

    dictionary = Dictionary([dict_entry_1, dict_entry_2, dict_entry_3, dict_entry_4, dict_entry_5], lang='latin')

    assert dictionary.filter_by_complex_condition('verb I').entries == [dict_entry_3]
    assert dictionary.filter_by_complex_condition('verb  I').entries == [dict_entry_3]
    assert dictionary.filter_by_complex_condition('verb I | verb II').entries == [dict_entry_3]
    assert dictionary.filter_by_complex_condition('verb I | verb III').entries == [dict_entry_3, dict_entry_4]
    assert dictionary.filter_by_complex_condition('I').entries == [dict_entry_3, dict_entry_5]
    assert dictionary.filter_by_complex_condition('I | verb III').entries == [dict_entry_3, dict_entry_5, dict_entry_4]
    assert dictionary.filter_by_complex_condition('verb I |  adv ').entries == [dict_entry_3, dict_entry_1, dict_entry_2]
    assert dictionary.filter_by_complex_condition('adv').entries == [dict_entry_1, dict_entry_2]
    assert dictionary.filter_by_complex_condition('adv| adv').entries == [dict_entry_1, dict_entry_2]
    assert dictionary.filter_by_complex_condition('adj').entries == []
