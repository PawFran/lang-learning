from sqlalchemy import Text
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Words(Base):
    __tablename__ = 'words'
    lang = Column(String, primary_key=True)
    word_id = Column(Integer, primary_key=True)
    part_of_speech = Column(String, ForeignKey('parts_of_speech.name'), primary_key=True)


class PartOfSpeech(Base):
    __tablename__ = 'parts_of_speech'
    name = Column(String, primary_key=True)


class Genre(Base):
    __tablename__ = 'genres'
    name = Column(String, primary_key=True, unique=True, nullable=False)


class LatinDeclension(Base):
    __tablename__ = 'latin_declensions'
    name = Column(String, primary_key=True, unique=True, nullable=False)


class LatinWordsTranslationsMapping(Base):
    __tablename__ = 'latin_words_translations_mapping'
    word_id = Column(Integer, primary_key=True)
    translation_id = Column(Integer, primary_key=True)
    part_of_speech = Column(String, primary_key=True)


class LatinVerbs(Base):
    __tablename__ = 'latin_verbs'
    id = Column(Integer, primary_key=True)
    base_word = Column(String, unique=True, nullable=False)
    base_word_acc = Column(String, nullable=False)
    infinite = Column(String, nullable=False)
    infinite_acc = Column(String, nullable=False)
    perfect = Column(String, nullable=False)
    perfect_acc = Column(String, nullable=False)
    supine = Column(String)
    supine_acc = Column(String)
    additional_info = Column(Text)
    conjugation = Column(String, ForeignKey('latin_conjugations.name'))


class LatinNouns(Base):
    __tablename__ = 'latin_nouns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, nullable=False)
    gen = Column(String, nullable=False)
    gen_acc = Column(String, nullable=False)
    declension = Column(String, ForeignKey('latin_declensions.name'), nullable=False)
    genre = Column(String, ForeignKey('genres.name'), nullable=False)
    only_pl = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('base', 'gen'),
    )


class LatinTranslations(Base):
    __tablename__ = 'latin_translations'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False, unique=True)
    example = Column(Text)
    associated_case = Column(Text)


class LatinConjugations(Base):
    __tablename__ = 'latin_conjugations'
    name = Column(String, primary_key=True)


class Language(Base):
    __tablename__ = 'languages'
    name = Column(String, primary_key=True)


engine = create_engine('sqlite:///lang_learning.sqlite')
Base.metadata.create_all(engine)
