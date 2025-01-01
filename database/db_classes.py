from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, event, Boolean
from sqlalchemy import Text, text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from common.lib.utils import DEFAULT_USER_NAME

Base = declarative_base()
views = []


class Languages(Base):
    __tablename__ = 'languages'
    name = Column(String, primary_key=True)


class PartsOfSpeech(Base):
    __tablename__ = 'parts_of_speech'

    name = Column(String, primary_key=True)


class Genres(Base):
    __tablename__ = 'genres'

    name = Column(String, primary_key=True, unique=True, nullable=False)


class LatinDeclensions(Base):
    __tablename__ = 'latin_declensions'

    name = Column(String, primary_key=True, unique=True, nullable=False)


class LatinConjugations(Base):
    __tablename__ = 'latin_conjugations'
    name = Column(String, primary_key=True)


class Words(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lang = Column(String, ForeignKey(f'{Languages.__tablename__}.name'), nullable=False)
    header = Column(Text, nullable=False)
    part_of_speech = Column(String, ForeignKey(f'{PartsOfSpeech.__tablename__}.name'), nullable=False)

    __table_args__ = (
        UniqueConstraint('lang', 'header', 'part_of_speech'),
    )


class Translations(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    translation = Column(Text, nullable=False, unique=True)
    example = Column(Text)
    associated_case = Column(Text)


class LatinWordsTranslationsMappings(Base):
    __tablename__ = 'latin_words_translations_mappings'

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), nullable=False)
    translation_id = Column(Integer, ForeignKey(f'{Translations.__tablename__}.id'), nullable=False)
    part_of_speech = Column(String, ForeignKey(f'{PartsOfSpeech.__tablename__}.name'), nullable=False)

    __table_args__ = (
        UniqueConstraint('word_id', 'translation_id', 'part_of_speech'),
    )


class LatinVerbs(Base):
    __tablename__ = 'latin_verbs'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    base_word = Column(String, nullable=False)
    base_word_acc = Column(String, nullable=False)
    infinite = Column(String, nullable=False)
    infinite_acc = Column(String, nullable=False)
    perfect = Column(String, nullable=False)
    perfect_acc = Column(String, nullable=False)
    supine = Column(String)
    supine_acc = Column(String)
    additional_info = Column(Text)
    conjugation = Column(String, ForeignKey(f'{LatinConjugations.__tablename__}.name'))

    __table_args__ = (
        UniqueConstraint('base_word_acc', 'infinite_acc', 'perfect_acc', 'supine_acc'),
    )


class LatinNouns(Base):
    __tablename__ = 'latin_nouns'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, nullable=False)
    gen = Column(String, nullable=False)
    gen_acc = Column(String, nullable=False)
    declension = Column(String, ForeignKey(f'{LatinDeclensions.__tablename__}.name'), nullable=False)
    genre = Column(String, ForeignKey(f'{Genres.__tablename__}.name'), nullable=False)
    only_pl = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('base_acc', 'gen_acc'),
    )


class LatinAdverbs(Base):
    __tablename__ = 'latin_adverbs'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinPrepositions(Base):
    __tablename__ = 'latin_prepositions'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinConjunctions(Base):
    __tablename__ = 'latin_conjunctions'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinPronouns(Base):
    __tablename__ = 'latin_pronouns'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    base = Column(String, nullable=False)
    base_acc = Column(String, unique=True, nullable=False)


class LatinAdjectives(Base):
    __tablename__ = 'latin_adjectives'

    id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'), primary_key=True)
    masculinum = Column(String, nullable=False)
    masculinum_acc = Column(String, nullable=False)
    femininum = Column(String, nullable=False)
    neutrum = Column(String, nullable=False)
    femininum_acc = Column(String, nullable=False)
    neutrum_acc = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('masculinum_acc', 'femininum_acc', 'neutrum_acc'),
    )


class TranslationResults(Base):
    __tablename__ = 'translation_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Text, nullable=False)
    session_id = Column(Integer, nullable=False)
    lang = Column(Text, ForeignKey(f'{Languages.__tablename__}.name'), nullable=False)
    word_pl = Column(Text,
                     nullable=False)  # foreign key was removed on purpose - words in dictionary are sometimes changed backwards
    expected_answer = Column(Text,
                             nullable=False)  # needs to be here - cannot take it from Words in view because some words may be added later and were not available during translations - to the result will be fdifferent
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)  # needs to be stored here, logic is to complex to calculate it in sql view
    time = Column(DateTime, nullable=False)


class TranslationExerciseCurrentSession(Base):
    __tablename__ = 'translation_exercise_current_session'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey(f'{Words.__tablename__}.id'))
    header = Column(Text, nullable=False)  # TODO FK to words ?
    part_of_speech = Column(String, ForeignKey(f'{PartsOfSpeech.__tablename__}.name'), nullable=False)
    translation = Column(Text, nullable=False)  # TODO FK to translations ?
    example = Column(Text)
    associated_case = Column(Text)
    is_active = Column(Boolean, default=False, nullable=False)  # New column to track active row
    user_name = Column(Text, default=DEFAULT_USER_NAME, nullable=False)
    session_id = Column(Integer, nullable=False)  # now always the same, but will make sense for multiple users


@event.listens_for(TranslationExerciseCurrentSession, "before_insert")
@event.listens_for(TranslationExerciseCurrentSession, "before_update")
def enforce_one_active(mapper, connection, target):
    if target.is_active:  # If the row being inserted/updated is set as active
        session = Session(bind=connection)  # Create a session for executing ORM operations

        # Set is_active = False for all other rows
        session.query(TranslationExerciseCurrentSession).filter(
            TranslationExerciseCurrentSession.id != target.id
        ).update({"is_active": False})

        session.commit()  # Commit changes to the database


### VIEWS
# Declarative View Base
class View:
    """Base class for SQLAlchemy views."""
    __abstract__ = True
    __view_name__ = None
    __view_query__ = None

    @classmethod
    def create_view(cls, engine):
        """Create the SQL view in the database."""
        if cls.__view_name__ and cls.__view_query__:
            with engine.begin() as conn:
                conn.execute(
                    text(f"CREATE OR REPLACE VIEW {cls.__view_name__} AS {cls.__view_query__}")
                )
            print(f"View '{cls.__view_name__}' created.")


# Views
class WordsWithTranslations(View):
    __view_name__ = "words_with_translations"
    __view_query__ = f"""
        SELECT w.id, header, w.part_of_speech, translation, example, associated_case 
        FROM {Words.__tablename__} w
        JOIN latin_words_translations_mappings m ON w.id = m.word_id
        JOIN translations t ON t.id = m.translation_id
    """


views.append(WordsWithTranslations)


class TranslationCorrectRatio(View):
    __view_name__ = "translation_correct_ratio"
    __view_query__ = f"""
        SELECT * FROM (
            SELECT word_pl, expected_answer, SUM(correct) AS correct, 
                   COUNT(*) - SUM(correct) AS incorrect, 
                   ROUND((SUM(correct) / COUNT(*))::NUMERIC * 100, 0) AS "correct %"
            FROM (
                SELECT *, CASE WHEN is_correct THEN 1 ELSE 0 END AS correct
                FROM {TranslationResults.__tablename__}
            ) subquery_1
            GROUP BY word_pl, expected_answer
        ) subquery_2
        ORDER BY "correct %" ASC, incorrect DESC, correct ASC
    """


views.append(TranslationCorrectRatio)


class TranslationLastAsked(View):
    __view_name__ = "translation_last_asked"
    __view_query__ = f"""
        SELECT word_pl, MAX(time) AS last_asked
        FROM {TranslationResults.__tablename__}
        GROUP BY word_pl
        ORDER BY last_asked ASC
    """


views.append(TranslationLastAsked)


class NextToBeAsked(View):
    __view_name__ = "next_to_be_asked"
    __view_query__ = f"""
        SELECT ratio.word_pl, expected_answer, last_asked, correct, incorrect, "correct %",
               ratio.idx AS correct_idx, last_asked.idx AS time_idx, 
               ratio.idx + last_asked.idx AS sum_idx
        FROM (
            SELECT *, ROW_NUMBER() OVER (ORDER BY last_asked ASC) AS idx
            FROM translation_last_asked
        ) last_asked
        JOIN (
            SELECT *, ROW_NUMBER() OVER (ORDER BY "correct %" ASC, incorrect DESC, correct ASC) AS idx
            FROM translation_correct_ratio
        ) ratio
        ON last_asked.word_pl = ratio.word_pl
        ORDER BY sum_idx ASC
    """


views.append(NextToBeAsked)


# Utility function to create all views
def create_all_views(engine):
    for view in views:
        view.create_view(engine)
