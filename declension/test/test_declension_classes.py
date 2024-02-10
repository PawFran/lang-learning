import os

import pytest

from declension.lib.declension_classes import *

path_to_declension_file = os.path.join('declension', 'resources', 'declension.json')

single_declension_pattern_dict = {
    "ancilla": {
        "first": {
            "femininum": {
                "singularis": {
                    "nominativus": "ancilla",
                    "genetivus": "ancillae",
                    "dativus": "ancillae",
                    "accusativus": "ancillam",
                    "ablativus": "ancillā",
                    "vocativus": "ancilla"
                },
                "pluralis": {
                    "nominativus": "ancilla",
                    "genetivus": "ancillārum",
                    "dativus": "ancillis",
                    "accusativus": "ancillas",
                    "ablativus": "ancillis",
                    "vocativus": "ancillae"
                }
            }
        }
    }
}

declension_dict_singular = single_declension_pattern_dict['ancilla']['first']['femininum']['singularis']
declension_dict_plural = single_declension_pattern_dict['ancilla']['first']['femininum']['pluralis']


def test_declension_type_from_dict():
    assert DeclensionType.from_string('first') is DeclensionType.I
    assert not DeclensionType.from_string('first') is DeclensionType.II
    assert DeclensionType.from_string('first ') is DeclensionType.I
    assert DeclensionType.from_string('First') is DeclensionType.I
    assert DeclensionType.from_string('i') is DeclensionType.I
    assert DeclensionType.from_string('I') is DeclensionType.I
    assert DeclensionType.from_string('1') is DeclensionType.I

    assert DeclensionType.from_string('third consonant') is DeclensionType.III_consonant
    assert DeclensionType.from_string('third_consonant') is DeclensionType.III_consonant
    assert DeclensionType.from_string('third-consonant') is DeclensionType.III_consonant

    assert DeclensionType.from_string('third vowel') is DeclensionType.III_vowel

    assert DeclensionType.from_string('relative') is DeclensionType.RELATIVE

    assert DeclensionType.from_string('relative') is not DeclensionType.III_vowel


def test_declension_type_from_dict_invalid():
    with pytest.raises(Exception):
        DeclensionType.from_string('firs')

    with pytest.raises(Exception):
        DeclensionType.from_string(None)

    with pytest.raises(Exception):
        DeclensionType.from_string(1)


def test_declension_pattern_from_dict():
    d = SingleDeclensionPattern.from_dict(single_declension_pattern_dict)

    # depends on test_declension_cases_from_dict
    cases_singular = declension_dict_singular
    cases_plural = declension_dict_plural

    assert d.base_word == 'ancilla'
    assert d.type is DeclensionType.I
    assert d.genre == 'femininum'
    assert d.singular == cases_singular
    assert d.plural == cases_plural


def test_declension_case_from_string():
    assert DeclensionCase.from_string('nominativus') is DeclensionCase.NOMINATIVUS
    assert DeclensionCase.from_string('genetivus') is DeclensionCase.GENETIVUS
    assert DeclensionCase.from_string('dative') is DeclensionCase.DATIVUS
    assert DeclensionCase.from_string('voc') is DeclensionCase.VOCATIVUS
    assert DeclensionCase.from_string('acc ') is DeclensionCase.ACCUSATIVUS


def test_declension_case_from_string_invalid():
    with pytest.raises(Exception):
        assert DeclensionCase.from_string('nominativues')


def test_parsing_full_declension_dict():
    # integration test - whether declension.json is parsed without errors
    dict_file_path = os.path.join("declension", "resources", "declension.json")

    Declensions.from_file_path(dict_file_path)


@pytest.mark.skip(reason="to be finished")
def test_declension_from_dict():
    d = Declensions.from_file_path(path_to_declension_file)

    declensions_sorted = sorted([*d.declensions])

    x = 1

    # first_declension = declensions_sorted


@pytest.mark.skip(reason="to be finished")
def test_group_declension_patterns_by_numbers():
    pass


@pytest.mark.skip(reason="to be finished")
def test_nth():
    pass
