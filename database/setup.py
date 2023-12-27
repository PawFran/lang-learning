from sqlalchemy import *

langs = ['latin', 'english']
latin_declensions = ['I', 'II', 'III vowel', 'III consonant', 'III mixed', 'IV', 'V']
latin_conjugations = ['I', 'II', 'III', 'IV']
parts_of_speech = ['verb', 'noun', 'adjective', 'adverb', 'preposition', 'conjuncture']
genres = ['masculine', 'feminine', 'neutral']

tables_with_enums = {
    'languages': langs,
    'parts_of_speech': parts_of_speech,
    'genres': genres,
    'latin_conjugations': latin_conjugations,
    'latin_declensions': latin_declensions
}

engine = create_engine('sqlite:///lang_learning.sqlite')

# begin() means autocommit at the end of the block
with engine.begin() as conn:    
    for t in tables_with_enums.keys():
        for x in tables_with_enums[t]:
            conn.execute(text(f"""INSERT OR IGNORE INTO {t} (name) VALUES ('{x}')"""))
    
    # print(result.all())
