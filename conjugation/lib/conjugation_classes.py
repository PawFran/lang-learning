import json
from dataclasses import dataclass
from enum import Enum

from numpy.random import default_rng


@dataclass
class ConjugationType(Enum):
    I = 'I'
    II = 'II'
    III = 'III'
    IV = 'IV'
    ANOMALOUS = 'ANOMALOUS'

    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').strip():
            case 'first' | 'i' | 'one' | '1':
                return ConjugationType.I
            case 'second' | 'ii' | 'two' | '2':
                return ConjugationType.II
            case 'third' | 'iii' | 'three' | '3':
                return ConjugationType.III
            case 'fourth' | 'iv' | 'three' | '4':
                return ConjugationType.IV
            case 'anom' | 'anomalous' | 'anomaly':
                return ConjugationType.ANOMALOUS
            case _:
                raise Exception(f'cannot parse string {s} to ConjugationType')


@dataclass
class Mood(Enum):
    Indicativus = 'indicative'
    Imperativus = 'imperative'
    Coniunctivus = 'subjunctive'

    # todo more will be added

    @staticmethod
    def from_string(s: str):
        match s.lower().strip():
            case 'indicativus' | 'indicative' | 'ind':
                return Mood.Indicativus
            case 'imperativus' | 'imperative' | 'imp':
                return Mood.Imperativus
            case 'coniunctivus' | 'subjunctive' | 'con' | 'sub':
                return Mood.Coniunctivus
            case _:
                raise Exception(f'cannot parse string {s} to Mood')


@dataclass
class Tense(Enum):
    Praesens = 'present'
    Imperfectum = 'imperfect'
    Futurum_I = 'future simple'
    Perfectum = 'perfect'
    Plusquamperfectum = 'pluperfect'
    Futurum_II = 'future perfect'

    # todo tests
    @staticmethod
    def from_string(s: str):
        match s.lower().replace('_', ' ').replace('-', ' ').replace('2', 'ii') \
            .replace('1', 'i').strip():
            case 'praesens' | 'present' | 'praes':
                return Tense.Praesens
            case 'imperfectum' | 'imperfect' | 'imperf':
                return Tense.Imperfectum
            case 'futurum i' | 'future i' | 'fut i' | 'future simple':
                return Tense.Futurum_I
            case 'perfectum' | 'perfect' | 'perf':
                return Tense.Perfectum
            case 'plusquamperfectum' | 'pluperfect' | 'pluperf' | 'plusquamperf':
                return Tense.Plusquamperfectum
            case 'futurum ii' | 'future ii' | 'fut ii' | 'future perfect':
                return Tense.Futurum_II
            case _:
                raise Exception(f'cannot parse string {s} to Tense')


@dataclass
class Voice(Enum):
    Activus = 'active'
    Passivus = 'passive'

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
    Singularis = 'singular'
    Pluralis = 'plural'

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
    First = '1'
    Second = '2'
    Third = '3'

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

    def summary(self):
        return f'''{self.infinitive} {self.mood.value.lower()} {self.tense.value} {self.voice.value.lower()} {self.person.value} {self.number.value.lower()}'''


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
        with open(json_file_path, encoding="utf8") as f:
            d = json.load(f)
            return ConjugationTable.from_dict(d)
