from sqlalchemy import Text, text, create_engine, Float, DateTime, inspect
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

DATABASE = 'sqlite:///lang_learning.sqlite'

Base = declarative_base()


class Words(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lang = Column(String, ForeignKey('languages.name'), nullable=False)
    header = Column(Text, nullable=False)
    part_of_speech = Column(String, ForeignKey('parts_of_speech.name'), nullable=False)

    __table_args__ = (
        UniqueConstraint('lang', 'header', 'part_of_speech'),
    )


class PartsOfSpeech(Base):
    __tablename__ = 'parts_of_speech'

    name = Column(String, primary_key=True)


class Genres(Base):
    __tablename__ = 'genres'

    name = Column(String, primary_key=True, unique=True, nullable=False)


class LatinDeclensions(Base):
    __tablename__ = 'latin_declensions'

    name = Column(String, primary_key=True, unique=True, nullable=False)


class LatinWordsTranslationsMappings(Base):
    __tablename__ = 'latin_words_translations_mappings'

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    translation_id = Column(Integer, ForeignKey('latin_translations.id'), nullable=False)
    part_of_speech = Column(String, ForeignKey('parts_of_speech.name'), nullable=False)

    __table_args__ = (
        UniqueConstraint('word_id', 'translation_id', 'part_of_speech'),
    )


class LatinVerbs(Base):
    __tablename__ = 'latin_verbs'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    base_word = Column(String, nullable=False)
    base_word_acc = Column(String, nullable=False)
    infinite = Column(String, nullable=False)
    infinite_acc = Column(String, nullable=False)
    perfect = Column(String, nullable=False)
    perfect_acc = Column(String, nullable=False)
    supine = Column(String)
    supine_acc = Column(String)
    additional_info = Column(Text)
    conjugation = Column(String, ForeignKey('latin_conjugations.name'))

    __table_args__ = (
        UniqueConstraint('base_word_acc', 'infinite_acc', 'perfect_acc', 'supine_acc'),
    )


class LatinNouns(Base):
    __tablename__ = 'latin_nouns'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, nullable=False)
    gen = Column(String, nullable=False)
    gen_acc = Column(String, nullable=False)
    declension = Column(String, ForeignKey('latin_declensions.name'), nullable=False)
    genre = Column(String, ForeignKey('genres.name'), nullable=False)
    only_pl = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('base_acc', 'gen_acc'),
    )


class LatinAdverbs(Base):
    __tablename__ = 'latin_adverbs'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinPrepositions(Base):
    __tablename__ = 'latin_prepositions'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinConjunctions(Base):
    __tablename__ = 'latin_conjunctions'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinPronouns(Base):
    __tablename__ = 'latin_pronouns'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinAdjectives(Base):
    __tablename__ = 'latin_adjectives'

    id = Column(Integer, ForeignKey('words.id'), primary_key=True)
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


class Languages(Base):
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
    time = Column(DateTime, nullable=False)

# Views
# class NounsWithTranslations(Base):
#     __tablename__ = 'nouns_with_translations'
#     __view_definition__ = '''
#         CREATE VIEW nouns_with_translations AS
#         SELECT base_acc, gen_acc, text, example
#         FROM latin_nouns n
#         JOIN words w ON n.id = w.external_word_id
#         JOIN latin_words_translations_mapping m ON w.id = m.word_id
#         JOIN latin_translations t ON m.translation_id = t.id;
#         '''
#
#     base_acc = Column(String, primary_key=True)
#     gen_acc = Column(String)
#     text = Column(String)
#     example = Column(String)


# class VerbsWithTranslations(Base):
#     __tablename__ = 'verbs_with_translations'
#     __view_definition__ = '''
#         CREATE VIEW verbs_with_translations AS
#         SELECT base_word_acc, infinite_acc, perfect_acc, supine_acc, conjugation, text, example
#         FROM latin_verbs v
#         JOIN words w ON v.id = w.external_word_id
#         JOIN latin_words_translations_mapping m ON w.id = m.word_id
#         JOIN latin_translations t ON m.translation_id = t.id
#         ORDER BY text;
#         '''
#
#     base_word_acc = Column(String, primary_key=True)
#     infinite_acc = Column(String)
#     perfect_acc = Column(String)
#     supine_acc = Column(String)
#     conjugation = Column(String)
#     text = Column(String)
#     example = Column(String)
#
#
# class TranslationLastCorrect(Base):
#     __tablename__ = 'translation_last_correct'
#     __view_definition__ = '''
#         CREATE VIEW translation_last_correct AS
#         SELECT word_pl, MAX(DATETIME(time)) AS last_correct
#         FROM translation_results
#         WHERE is_correct = "True"
#         GROUP BY word_pl
#         ORDER BY last_correct DESC;
#         '''
#
#     word_pl = Column(String, primary_key=True)
#     last_correct = Column(DateTime)
#
#
# class TranslationCorrectRatio(Base):
#     __tablename__ = 'translation_correct_ratio'
#     __view_definition__ = '''
#         CREATE VIEW translation_correct_ratio AS
#         SELECT *
#         FROM (
#             SELECT word_pl, correct_translation, SUM(correct) AS correct,
#                    COUNT(*) - SUM(correct) AS incorrect,
#                    ROUND(SUM(correct) / CAST(COUNT(*) AS REAL) * 100, 0) AS "correct %"
#             FROM (
#                 SELECT *,
#                        CASE WHEN LOWER(is_correct) = 'true' THEN 1 ELSE 0 END AS correct
#                 FROM translation_results
#             )
#             GROUP BY word_pl
#         )
#         ORDER BY "correct %" ASC, incorrect DESC, correct ASC;
#         '''
#
#     word_pl = Column(String, primary_key=True)
#     correct_translation = Column(String)
#     correct = Column(Integer)
#     incorrect = Column(Integer)
#     correct_percentage = Column(Float, name='"correct %"')
#
#
# class TranslationStatistics(Base):
#     __tablename__ = 'translation_statistics'
#     __view_definition__ = '''
#         CREATE VIEW translation_statistics AS
#         SELECT ratio.word_pl, correct_translation, correct, incorrect, "correct %", last_correct
#         FROM translation_correct_ratio ratio
#         LEFT JOIN translation_last_correct last
#         ON last.word_pl = ratio.word_pl;
#         '''
#
#     word_pl = Column(String, primary_key=True)
#     correct_translation = Column(String)
#     correct = Column(Integer)
#     incorrect = Column(Integer)
#     correct_percentage = Column(Float, name='"correct %"')
#     last_correct = Column(DateTime)

# Utility function to create views
def create_views(engine, base):
    """Execute CREATE VIEW statements for all classes with __view_definition__."""
    with engine.connect() as connection:
        for cls in base.__subclasses__():
            if hasattr(cls, '__view_definition__'):
                connection.execute(text(cls.__view_definition__))

def drop_all_views(engine):
    with engine.connect() as conn:
        # Drop views
        inspector = inspect(engine)
        for view_name in inspector.get_view_names():
            conn.execute(text(f"DROP VIEW IF EXISTS {view_name}"))
            print(f"View {view_name} dropped")
