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

json_file_path = os.path.join("conjugation", "test", "resources", "conjugation.json")
with open(json_file_path, encoding="utf8") as f:
    test_dict = json.load(f)


def test_conjugation_type_from_dict():
    assert ConjugationType.from_string('first') is ConjugationType.I
    assert ConjugationType.from_string('first ') is ConjugationType.I
    assert ConjugationType.from_string('First') is ConjugationType.I
    assert ConjugationType.from_string('i') is ConjugationType.I
    assert ConjugationType.from_string('I') is ConjugationType.I
    assert ConjugationType.from_string('1') is ConjugationType.I
    assert ConjugationType.from_string('4') is ConjugationType.IV
    assert ConjugationType.from_string('anom') is ConjugationType.ANOMALOUS
    assert ConjugationType.from_string('anomalous') is ConjugationType.ANOMALOUS
    assert ConjugationType.from_string('anomaly') is ConjugationType.ANOMALOUS

    assert not ConjugationType.from_string('first') is ConjugationType.II


def test_conjugation_type_from_dict_invalid():
    with pytest.raises(Exception):
        ConjugationType.from_string('firs')

    with pytest.raises(Exception):
        ConjugationType.from_string(None)

    with pytest.raises(Exception):
        ConjugationType.from_string(1)


def test_mood_from_string():
    assert Mood.from_string('indicativus') is Mood.Indicativus
    assert Mood.from_string('indicativus ') is Mood.Indicativus
    assert Mood.from_string('  Indicativus ') is Mood.Indicativus
    assert Mood.from_string('  Ind') is Mood.Indicativus

    assert Mood.from_string('  imperativus') is Mood.Imperativus

    assert not Mood.from_string('indicativus') is Mood.Imperativus


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
    assert first_record.conjugation_type is ConjugationType.I
    assert first_record.mood is Mood.Indicativus
    assert first_record.tense is Tense.Praesens
    assert first_record.voice is Voice.Activus
    assert first_record.number is Number.Singularis
    assert first_record.person is Person.First
    assert first_record.word == 'laudo'

    last_but_one_record = table.records[-1]
    assert last_but_one_record.infinitive == 'audīre'
    assert last_but_one_record.conjugation_type is ConjugationType.IV
    assert last_but_one_record.mood is Mood.Imperativus
    assert last_but_one_record.tense is Tense.Praesens
    assert last_but_one_record.voice is Voice.Passivus
    assert last_but_one_record.number is Number.Pluralis
    assert last_but_one_record.person is Person.Second
    assert last_but_one_record.word == 'audimini'


def test_enum_short():
    assert Mood.Indicativus.short() == 'ind'
    assert Mood.Imperativus.short() == 'imp'
    assert Mood.Coniunctivus.short() == 'sub'

    assert Tense.Praesens.short() == 'pres'
    assert Tense.Imperfectum.short() == 'imperf'
    assert Tense.Perfectum.short() == 'perf'

    assert Voice.Activus.short() == 'act'
    assert Voice.Passivus.short() == 'pass'
