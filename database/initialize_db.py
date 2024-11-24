import subprocess

from sqlalchemy import *

from database.migration_dictionary import migrate_dictionary
from database.migration_translation_results import migrate_translation_results
from db_classes import Base, create_views
from vocabulary.lib.dict_classes import PartOfSpeech
from utils import DATABASE, DB_FILE_NAME
import os

from vocabulary.lib.parsing_args import parse_args

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

def remove_db():
    if os.path.exists(DB_FILE_NAME):
        os.remove(DB_FILE_NAME)
        print(f'{DB_FILE_NAME} removed')
    else:
        print(f'{DB_FILE_NAME} does not exist')

if __name__ == '__main__':
    remove_db()

    engine = create_engine(DATABASE)
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

    migrate_dictionary()
    print('dictionary migrated')

    migrate_translation_results()
    print('translation results migrated')
