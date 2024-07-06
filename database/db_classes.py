from sqlalchemy import Text
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
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


class LatinAdverbs(Base):
    __tablename__ = 'latin_adverbs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinPrepositions(Base):
    __tablename__ = 'latin_prepositions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinConjunctions(Base):
    __tablename__ = 'latin_conjunctions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinPronouns(Base):
    __tablename__ = 'latin_pronouns'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinAdjectives(Base):
    __tablename__ = 'latin_adjectives'

    id = Column(Integer, primary_key=True, autoincrement=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


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


class TranslationResult(Base):
    __tablename__ = 'translation_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Text, nullable=False)
    session_id = Column(Integer, nullable=False)
    lang = Column(Text, nullable=False)
    word_pl = Column(Text, nullable=False)
    correct_translation = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Text, nullable=False)
    time = Column(Text, nullable=False)


engine = create_engine('sqlite:///lang_learning.sqlite')
Base.metadata.create_all(engine)
