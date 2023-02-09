import pytest
import os

from latin_grammar.lib.declension_classes import *

path_to_declension_file = os.path.join('latin_grammar', 'resources', 'declension.json')

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

declension_dict_invalid = {
    "nominativus": "ancilla",
    "genetivus": "ancillae",
}


def test_declension_cases_from_dict():
    d = DeclensionCasesDict.from_dict(declension_dict_singular)
    assert d.nominativus == "ancilla"
    assert d.genetivus == "ancillae"
    assert d.dativus == "ancillae"
    assert d.accusativus == "ancillam"
    assert d.ablativus == "ancillā"
    assert d.vocativus == "ancilla"


def test_declension_cases_invalid():
    with pytest.raises(Exception):
        DeclensionCasesDict.from_dict(declension_dict_invalid)


def test_declension_pattern_from_dict():
    d = SingleDeclensionPattern.from_dict(single_declension_pattern_dict)

    # depends on test_declension_cases_from_dict
    cases_singular = DeclensionCasesDict.from_dict(declension_dict_singular)
    cases_plural = DeclensionCasesDict.from_dict(declension_dict_plural)

    assert d.base_word == 'ancilla'
    assert d.number == 'first'
    assert d.genre == 'femininum'
    assert d.singular == cases_singular
    assert d.plural == cases_plural


@pytest.mark.skip(reason="to be finished")
def test_declension_from_dict():
    d = DeclensionDict.from_file_path(path_to_declension_file)

    declensions_sorted = sorted([*d.declensions])

    x = 1

    # first_declension = declensions_sorted


@pytest.mark.skip(reason="to be finished")
def test_group_declension_patterns_by_numbers():
    pass


@pytest.mark.skip(reason="to be finished")
def test_nth():
    pass
