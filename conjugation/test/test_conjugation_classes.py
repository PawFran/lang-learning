import pytest

from conjugation.lib.conjugation_classes import *


def test_conjugation_type_from_dict():
    assert ConjugationType.from_string('first') == ConjugationType.I
    assert ConjugationType.from_string('first ') == ConjugationType.I
    assert ConjugationType.from_string('First') == ConjugationType.I
    assert ConjugationType.from_string('i') == ConjugationType.I
    assert ConjugationType.from_string('I') == ConjugationType.I
    assert ConjugationType.from_string('1') == ConjugationType.I

    assert ConjugationType.from_string('third a') == ConjugationType.IIIa
    assert ConjugationType.from_string('third_a') == ConjugationType.IIIa
    assert ConjugationType.from_string('third-a') == ConjugationType.IIIa

    assert ConjugationType.from_string('third b') == ConjugationType.IIIb


def test_conjugation_type_from_dict_invalid():
    with pytest.raises(Exception):
        ConjugationType.from_string('firs')

    with pytest.raises(Exception):
        ConjugationType.from_string(None)

    with pytest.raises(Exception):
        ConjugationType.from_string(1)


def test_mood_from_string():
    assert Mood.from_string('indicativus') == Mood.Indicativus
    assert Mood.from_string('indicativus ') == Mood.Indicativus
    assert Mood.from_string('  Indicativus ') == Mood.Indicativus
    assert Mood.from_string('  Ind') == Mood.Indicativus

    assert Mood.from_string('  imperativus') == Mood.Imperativus


def test_mood_from_string_invalid():
    with pytest.raises(Exception):
        Mood.from_string('in')

    with pytest.raises(Exception):
        Mood.from_string(None)

    with pytest.raises(Exception):
        Mood.from_string(1)
