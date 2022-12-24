from dataclasses import dataclass


@dataclass
class AbstractWord:
    base: str
    # method for printing additional info specific for subtypes ?
    # add parse method


@dataclass
class Verb(AbstractWord):
    conjugation: str  # maybe another class/enum ?
    infinite: str
    perfect: str
    supine: str


@dataclass
class Noun(AbstractWord):
    declension: str  # roman number
    genetive: str
    genre: str
    only_plural: bool = False


@dataclass
class Adverb(AbstractWord):
    # TODO TBD
    pass


@dataclass
class Adjective(AbstractWord):
    # TODO TBD
    pass


@dataclass
class DictEntry:
    """storing entries like:
    castīgo, āre, avi, atum [verb] [I]
    (Ancillam miseram domina sevēra castīgat)
    1. karać
    """
    word: AbstractWord
    example: str
    translations: list[str]


@dataclass
class Dict:
    """full dictionary"""
    entries: list[DictEntry]
