import psycopg2
from sqlalchemy import *
from sqlalchemy_utils import database_exists, create_database

from conjugation.lib.conjugation_classes import ConjugationType, Mood, Number, Tense, Voice, Person
from database.db_classes import Base, create_all_views, Languages, PartsOfSpeech, Genres, LatinConjugations, \
    LatinDeclensions, DeclensionCases, Moods, Tenses, Voices, Numbers, Persons
from database.migration_dictionary import migrate_dictionary
from database.migration_exercise_results import migrate_translation_exercise_results, \
    migrate_declension_exercise_results
from database.migration_patterns import migrate_declension_patterns, migrate_conjugation_patterns
from declension.lib.declension_classes import DeclensionType, DeclensionCase, Genre
from vocabulary.lib.dict_classes import PartOfSpeech, Lang


def values_from(enum_class):
    return [x.value for x in enum_class]


tables_with_enums = {
    Languages.__tablename__: values_from(Lang),
    DeclensionCases.__tablename__: values_from(DeclensionCase),
    PartsOfSpeech.__tablename__: values_from(PartOfSpeech),
    Genres.__tablename__: values_from(Genre),
    Moods.__tablename__: values_from(Mood),
    Tenses.__tablename__: values_from(Tense),
    Voices.__tablename__: values_from(Voice),
    Numbers.__tablename__: values_from(Number),
    Persons.__tablename__: values_from(Person),
    LatinDeclensions.__tablename__: values_from(DeclensionType),
    LatinConjugations.__tablename__: values_from(ConjugationType),
}


def initialize_database(engine: Engine,
                        remove_old: bool,
                        dictionary_migration: bool,
                        declension_patterns_migration: bool,
                        conjugation_patterns_migration: bool,
                        translation_exercise_results_migration: bool,
                        declension_exercise_results_migration: bool,
                        dictionary_folder: str,
                        declension_patterns_file_path: str,
                        conjugation_patterns_file_path: str,
                        translation_exercise_results_path: str,
                        declension_exercise_results_path: str
                        ):
    if remove_old:
        remove_db(engine)

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)
    print('All tables created')

    create_all_views(engine)
    print('All views created')

    # begin() means autocommit at the end of the block
    with engine.begin() as conn:
        for t in tables_with_enums.keys():
            for x in tables_with_enums[t]:
                conn.execute(
                    text(f"INSERT INTO {t} (name) VALUES (:value) ON CONFLICT DO NOTHING"),
                    {"value": x}
                )
    print('All initial values inserted')

    if dictionary_migration:
        migrate_dictionary(engine, dictionary_folder)
        print('dictionary migrated')

    if declension_patterns_migration:
        migrate_declension_patterns(engine, declension_patterns_file_path)
        print('declension patterns migrated')

    if conjugation_patterns_migration:
        migrate_conjugation_patterns(engine, conjugation_patterns_file_path)
        print('conjugation patterns migrated')

    if translation_exercise_results_migration:
        migrate_translation_exercise_results(engine, translation_exercise_results_path)
        print('translation exercise results migrated')

    if declension_exercise_results_migration:
        migrate_declension_exercise_results(engine, declension_exercise_results_path)
        print('declension exercise results migrated')


def remove_db(engine):
    db_name = engine.url.database

    # Extract connection details from the engine
    user = engine.url.username
    password = engine.url.password
    host = engine.url.host
    port = engine.url.port

    # Connect to the `postgres` database for administrative commands
    conn = psycopg2.connect(
        dbname='postgres',  # Use a default admin database
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.set_session(autocommit=True)  # Enable autocommit mode

    try:
        cursor = conn.cursor()
        # Terminate other connections to the target database
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
              AND pid <> pg_backend_pid();
        """)
        # Drop the database
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"Database {db_name} removed")
        cursor.close()
    finally:
        conn.close()
