import os

import pytest

from conjugation.lib.conjugation_classes import *

small_test_dict = {
    "laudāre": {
        "first": {
            "indicativus": {
                "praesens": {
                    "activus": {
                        "singularis": {
                            "first": "laudo",
                            "second": "laudas",
                            "third": "laudat"
                        },
                        "pluralis": {
                            "first": "laudāmus",
                            "second": "laudātis",
                            "third": "laudant"
                        }
                    },
                },
            },
        },
    },
}

json_file_path = os.path.join("conjugation", "resources", "conjugation.json")
with open(json_file_path) as f:
    test_dict = json.load(f)


def test_conjugation_type_from_dict():
    assert ConjugationType.from_string('first') == ConjugationType.I
    assert ConjugationType.from_string('first ') == ConjugationType.I
    assert ConjugationType.from_string('First') == ConjugationType.I
    assert ConjugationType.from_string('i') == ConjugationType.I
    assert ConjugationType.from_string('I') == ConjugationType.I
    assert ConjugationType.from_string('1') == ConjugationType.I

    # assert ConjugationType.from_string('third a') == ConjugationType.IIIa
    # assert ConjugationType.from_string('third_a') == ConjugationType.IIIa
    # assert ConjugationType.from_string('third-a') == ConjugationType.IIIa

    # assert ConjugationType.from_string('third b') == ConjugationType.IIIb


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


def test_small_conjugation_table_from_dict():
    small_table = ConjugationTable.from_dict(small_test_dict)
    assert len(small_table.records) == 6


def test_conjugation_table_from_dict():
    table = ConjugationTable.from_dict(test_dict)

    first_record = table.records[0]

    assert first_record.infinitive == 'laudāre'
    assert first_record.conjugation_type == ConjugationType.I
    assert first_record.mood == Mood.Indicativus
    assert first_record.tense == Tense.Praesens
    assert first_record.voice == Voice.Activus
    assert first_record.number == Number.Singularis
    assert first_record.person == Person.First
    assert first_record.word == 'laudo'

    last_but_one_record = table.records[-1]
    assert last_but_one_record.infinitive == 'audīre'
    assert last_but_one_record.conjugation_type == ConjugationType.IV
    assert last_but_one_record.mood == Mood.Imperativus
    assert last_but_one_record.tense == Tense.Praesens
    assert last_but_one_record.voice == Voice.Passivus
    assert last_but_one_record.number == Number.Pluralis
    assert last_but_one_record.person == Person.Second
    assert last_but_one_record.word == 'audimini'
