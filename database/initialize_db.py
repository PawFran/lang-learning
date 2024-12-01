import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import *

from database.migration_dictionary import migrate_dictionary
from database.migration_translation_results import migrate_translation_results
from database.db_classes import Base, create_views, DB_FILE_NAME
from vocabulary.lib.dict_classes import PartOfSpeech

langs = ['latin', 'english']
latin_declensions = ['I', 'II', 'III', 'III vowel', 'III consonant', 'III mixed', 'IV', 'V']
latin_conjugations = ['I', 'II', 'III', 'IV', 'ANOMALOUS']
parts_of_speech = [p.value for p in PartOfSpeech]
genres = ['masculine', 'feminine', 'neutral', 'masculine and feminine']

tables_with_enums = {
    'languages': langs,
    'parts_of_speech': parts_of_speech,
    'genres': genres,
    'latin_conjugations': latin_conjugations,
    'latin_declensions': latin_declensions
}


def remove_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f'{db_path} removed')
    else:
        print(f'{db_path} does not exist')


def initialize_database(db_path: str, remove_old: bool, dictionary_migration: bool, translation_results_migration: bool,
                        dictionary_folder: str = None, translation_results_folder: str = None):

    if remove_old:
        remove_db(db_path)

    db = f'sqlite:///{db_path}'
    engine = create_engine(db)
    print(f'create engine for {db}')

    Base.metadata.create_all(engine)
    print('All tables created')

    create_views(engine)
    print('All views created')

    # begin() means autocommit at the end of the block
    with engine.begin() as conn:
        for t in tables_with_enums.keys():
            for x in tables_with_enums[t]:
                conn.execute(text(f"""INSERT OR IGNORE INTO {t} (name) VALUES ('{x}')"""))
    print('All initial values inserted')

    if dictionary_migration:
        migrate_dictionary(engine, dictionary_folder)
        print('dictionary migrated')

    if translation_results_migration:
        migrate_translation_results(engine, translation_results_folder)
        print('translation results migrated')


if __name__ == '__main__':
    dict_folder = os.path.join('..', 'vocabulary', 'dicts')
    translation_results_dir = os.path.join('..', 'vocabulary', 'db')
    initialize_database(db_path=DB_FILE_NAME,remove_old=True, dictionary_migration=True, translation_results_migration=True,
                        dictionary_folder=dict_folder, translation_results_folder=translation_results_dir)
