from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, event, Boolean
from sqlalchemy import Text, text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from common.lib.utils import DEFAULT_USER_NAME

# DB_FILE_NAME = 'lang_learning.sqlite'
# DATABASE = f'sqlite:///{DB_FILE_NAME}'

Base = declarative_base()


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
    word_pl = Column(Text, nullable=False) # foreign key was removed on purpose - words in dictionary are sometimes changed backwards
    expected_answer = Column(Text,
                             nullable=False)  # needs to be here - cannot take it from Words in view because some words may be added later and were not available during translations - to the result will be fdifferent
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Text, nullable=False)  # needs to be store here, logic is to complex to calculate it in sql view
    time = Column(DateTime, nullable=False)


class TranslationExerciseCurrentSession(Base):
    __tablename__ = 'translation_exercise_current_session'

    id = Column(Integer, primary_key=True)  # no autoincrement
    header = Column(Text, nullable=False)  # TODO FK to words ?
    part_of_speech = Column(String, ForeignKey(f'{PartsOfSpeech.__tablename__}.name'), nullable=False)
    translation = Column(Text, nullable=False)  # TODO FK to translations ?
    example = Column(Text)
    associated_case = Column(Text)
    is_active = Column(Boolean, default=False, nullable=False)  # New column to track active row
    user_name = Column(Text, default=DEFAULT_USER_NAME, nullable=False)
    session_id = Column(Integer, nullable=False) # now always the same, but will make sense for multiple users


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
create_view_statement = 'CREATE VIEW words_with_translations as'

view_words_with_translations_select = f'''
            select w.id, header, w.part_of_speech, translation, example, associated_case from {Words.__tablename__} w
            join {LatinWordsTranslationsMappings.__tablename__} m on w.id = m.word_id
            join {Translations.__tablename__} t on t.id = m.translation_id
        '''


# Utility function to create views
def create_views(engine):
    with engine.connect() as connection:
        ### words_with_translations
        connection.execute(text(create_view_statement + '\n' + view_words_with_translations_select))

        ### translation_correct_ratio
        connection.execute(text(f'''
            CREATE VIEW translation_correct_ratio as
            select * from
                (select word_pl, expected_answer, sum(correct) as correct, count(*) - sum(correct) as incorrect, round((sum(correct) / count(*))::numeric * 100, 0) as "correct %" FROM
                    (SELECT *,
                        CASE WHEN LOWER(is_correct) = 'true' THEN 1 ELSE 0 END AS correct
                    from {TranslationResults.__tablename__}) as subquery_1 
                group by word_pl, expected_answer) as subquery_2
            order by "correct %" asc, incorrect desc, correct asc
        '''))

        ### translation_last_asked
        connection.execute(text(f'''
            CREATE VIEW translation_last_asked as
            select word_pl, max(time) as last_asked
            from {TranslationResults.__tablename__}
            group by word_pl
            order by last_asked asc
        '''))

        ### next_to_be_asked
        connection.execute(text(f'''
            create view next_to_be_asked as
            select ratio.word_pl, expected_answer, last_asked, correct, incorrect, "correct %", ratio.idx as correct_idx, last_asked.idx as time_idx, ratio.idx + last_asked.idx as sum_idx
            from ( 
                select *, ROW_NUMBER() over (order by last_asked asc) as idx 
                from translation_last_asked
                ) last_asked
            join (
                select *, ROW_NUMBER() over (order by "correct %" asc, incorrect desc, correct asc) as idx 
                from translation_correct_ratio
                ) ratio
            on last_asked.word_pl = ratio.word_pl
            order by sum_idx asc
        '''))
