import json
from dataclasses import dataclass
from enum import Enum

from numpy.random import default_rng


@dataclass
class ConjugationType(Enum):
    I = 1
    II = 2
    III = 3
    # IIIa = 3.1
    # IIIb = 3.2
    IV = 4

    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').strip():
            case 'first' | 'i' | 'one' | '1':
                return ConjugationType.I
            case 'second' | 'ii' | 'two' | '2':
                return ConjugationType.II
            case 'third' | 'iii' | 'three' | '3':
                return ConjugationType.III
            case 'fourth' | 'iv' | 'three' | '3':
                return ConjugationType.IV
            case _:
                raise Exception(f'cannot parse string {s} to ConjugationType')


@dataclass
class Mood(Enum):
    Indicativus = 1
    Imperativus = 2

    # todo more will be added

    @staticmethod
    def from_string(s: str):
        match s.lower().strip():
            case 'indicativus' | 'indicative' | 'ind':
                return Mood.Indicativus
            case 'imperativus' | 'imperative' | 'imp':
                return Mood.Imperativus
            case _:
                raise Exception(f'cannot parse string {s} to Mood')


@dataclass
class Tense(Enum):
    Praesens = 1
    Imperfectum = 2
    Futurum_I = 3
    Perfectum = 4
    Plusquamperfectum = 5
    Futurum_II = 6

    # todo tests
    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').strip():
            case 'praesens' | 'present':
                return Tense.Praesens
            case 'imperfectum' | 'imperfect':
                return Tense.Imperfectum
            case 'futurum i' | 'future i':
                return Tense.Futurum_I
            case 'perfectum' | 'perfect':
                return Tense.Perfectum
            case 'plusquamperfectum' | 'pluperfect':
                return Tense.Plusquamperfectum
            case 'futurum ii' | 'future ii':
                return Tense.Futurum_II
            case _:
                raise Exception(f'cannot parse string {s} to Tense')


@dataclass
class Voice(Enum):
    Activus = 1
    Passivus = 2

    @staticmethod
    def from_string(s: str):
        match s.lower().strip():
            case 'activus' | 'active' | 'act':
                return Voice.Activus
            case 'passivus' | 'passive' | 'pass':
                return Voice.Passivus
            case _:
                raise Exception(f'cannot parse string {s} to Voice')


@dataclass
class Number(Enum):
    Singularis = 1
    Pluralis = 2

    @staticmethod
    def from_string(s: str):
        match s.lower().strip():
            case 'singularis' | 'singular' | 'sing':
                return Number.Singularis
            case 'pluralis' | 'plural' | 'pl':
                return Number.Pluralis
            case _:
                raise Exception(f'cannot parse string {s} to Number')


@dataclass
class Person(Enum):
    First = 1
    Second = 2
    Third = 3

    @staticmethod
    def from_string(s: str):
        match s.lower().strip():
            case 'first' | 'one' | '1':
                return Person.First
            case 'second' | 'two' | '2':
                return Person.Second
            case 'third' | 'three' | '3':
                return Person.Third
            case _:
                raise Exception(f'cannot parse string {s} to Person')


@dataclass
class SingleConjugationRecord:
    infinitive: str
    conjugation_type: ConjugationType
    mood: Mood
    tense: Tense
    voice: Voice
    number: Number
    person: Person
    word: str


class ConjugationTable:

    def __init__(self, records: list[SingleConjugationRecord]):
        self.records = records

    def random_record(self, rng=default_rng()) -> SingleConjugationRecord:
        if len(self.records) == 0:
            raise Exception("cannot select random entry from empty dict")

        return rng.choice(self.records)

    @staticmethod
    def from_dict(d: dict):
        records: list[SingleConjugationRecord] = []
        all_infinitives = [*d]
        for i in range(len(all_infinitives)):
            infinitive = all_infinitives[i]
            conjugation_type = [*d[infinitive]][0]  # always one for given word
            all_moods = [*d[infinitive][conjugation_type]]
            for j in range(len(all_moods)):
                mood = all_moods[j]
                all_tenses = [*d[infinitive][conjugation_type][mood]]
                for k in range(len(all_tenses)):
                    tense = all_tenses[k]
                    all_voices = [*d[infinitive][conjugation_type][mood][tense]]
                    for v in range(len(all_voices)):
                        voice = all_voices[v]
                        all_numbers = [*d[infinitive][conjugation_type][mood][tense][voice]]
                        for n in range(len(all_numbers)):
                            number = all_numbers[n]
                            all_persons = [*d[infinitive][conjugation_type][mood][tense][voice][number]]
                            for p in range(len(all_persons)):
                                person = all_persons[p]
                                word = d[infinitive][conjugation_type][mood][tense][voice][number][person]

                                current_record = SingleConjugationRecord(
                                    infinitive,
                                    ConjugationType.from_string(conjugation_type),
                                    Mood.from_string(mood),
                                    Tense.from_string(tense),
                                    Voice.from_string(voice),
                                    Number.from_string(number),
                                    Person.from_string(person),
                                    word
                                )

                                records.append(current_record)

        return ConjugationTable(records)

    @staticmethod
    def from_file_path(json_file_path: str):
        with open(json_file_path) as f:
            d = json.load(f)
            return ConjugationTable.from_dict(d)
