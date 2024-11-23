from sqlalchemy import *

from database.db_classes import drop_all_views
from db_classes import Base, create_views
from vocabulary.lib.dict_classes import PartOfSpeech
from utils import DATABASE

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

if __name__ == '__main__':
    engine = create_engine(DATABASE)
    drop_all_views(engine)
    Base.metadata.drop_all(engine)
    print('All existing tables dropped')
    Base.metadata.create_all(engine)
    print('All tables created')
    # create_views(engine, Base)
    # print('All views created')

    # begin() means autocommit at the end of the block
    with engine.begin() as conn:
        for t in tables_with_enums.keys():
            for x in tables_with_enums[t]:
                conn.execute(text(f"""INSERT OR IGNORE INTO {t} (name) VALUES ('{x}')"""))

    print('All initial values inserted (but it\'s now full migration!)')
