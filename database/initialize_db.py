# Allow imports to work when run from either top level or current directory
import sys
from pathlib import Path

import psycopg2
from sqlalchemy_utils import database_exists, create_database

# Add project root to path if running from database/ directory
current_dir = Path(__file__).parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from database.migration_dictionary import migrate_dictionary
from database.migration_exercise_results import *
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
    LatinDeclensionTypes.__tablename__: values_from(DeclensionType),
    LatinConjugationTypes.__tablename__: values_from(ConjugationType),
}

# needs to be invoked from project root
dictionary_folder = os.path.join('vocabulary', 'dicts')

declension_patterns_file_path = os.path.join("declension", "resources", "declension.json")
conjugation_patterns_file_path = os.path.join("conjugation", "resources", "conjugation.json")

translation_exercise_results_path = os.path.join('vocabulary', 'db', 'translation_exercise_results.csv')
reversed_translation_exercise_results_path = os.path.join('vocabulary', 'db',
                                                          'reversed_translation_exercise_results.csv')
declension_exercise_results_path = os.path.join('vocabulary', 'db', 'declension_exercise_results.csv')
conjugation_exercise_results_path = os.path.join('vocabulary', 'db', 'conjugation_exercise_results.csv')

declension_exercise_session_metadata_path = os.path.join('vocabulary', 'db', 'declension_exercise_session_metadata.csv')
conjugation_exercise_session_metadata_path = os.path.join('vocabulary', 'db',
                                                          'conjugation_exercise_session_metadata.csv')
translation_exercise_session_metadata_path = os.path.join('vocabulary', 'db',
                                                          'translation_exercise_session_metadata.csv')
reversed_translation_exercise_session_metadata_path = os.path.join('vocabulary', 'db',
                                                                   'reversed_translation_exercise_session_metadata.csv')


def initialize_database(engine: Engine,
                        remove_old: bool,
                        dictionary_migration: bool,
                        declension_patterns_migration: bool,
                        conjugation_patterns_migration: bool,
                        translation_exercise_results_migration: bool,
                        reversed_translation_exercise_results_migration: bool,
                        declension_exercise_results_migration: bool,
                        conjugation_exercise_results_migration: bool,
                        declension_exercise_session_metadata_migration: bool,
                        conjugation_exercise_session_metadata_migration: bool,
                        translation_exercise_session_metadata_migration: bool,
                        reversed_translation_exercise_session_metadata_migration: bool
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

    if reversed_translation_exercise_results_migration:
        migrate_reversed_translation_exercise_results(engine, reversed_translation_exercise_results_path)
        print('translation exercise results migrated')

    if declension_exercise_results_migration:
        migrate_declension_exercise_results(engine, declension_exercise_results_path)
        print('declension exercise results migrated')

    if conjugation_exercise_results_migration:
        migrate_conjugation_exercise_results(engine, conjugation_exercise_results_path)
        print('conjugation exercise results migrated')

    if declension_exercise_session_metadata_migration:
        migrate_declension_exercise_session_metadata(engine, declension_exercise_session_metadata_path)
        print('declension exercise session metadata migrated')

    if conjugation_exercise_session_metadata_migration:
        migrate_conjugation_exercise_session_metadata(engine, conjugation_exercise_session_metadata_path)
        print('conjugation exercise session metadata migrated')

    if translation_exercise_session_metadata_migration:
        migrate_translation_exercise_session_metadata(engine, translation_exercise_session_metadata_path)
        print('translation exercise session metadata migrated')

    if reversed_translation_exercise_session_metadata_migration:
        migrate_reversed_translation_exercise_session_metadata(engine,
                                                               reversed_translation_exercise_session_metadata_path)
        print('reversed translation exercise session metadata migrated')


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


def default_db_initialization():
    from environment import engine

    initialize_database(engine=engine,
                        remove_old=True,
                        dictionary_migration=True,
                        declension_patterns_migration=True,
                        conjugation_patterns_migration=True,
                        translation_exercise_results_migration=True,
                        reversed_translation_exercise_results_migration=True,
                        declension_exercise_results_migration=True,
                        conjugation_exercise_results_migration=True,
                        declension_exercise_session_metadata_migration=True,
                        conjugation_exercise_session_metadata_migration=True,
                        translation_exercise_session_metadata_migration=True,
                        reversed_translation_exercise_session_metadata_migration=True)


# needs to be invoked from project root
if __name__ == '__main__':
    default_db_initialization()
