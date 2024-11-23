from sqlalchemy import *

tables_to_be_cleaned = ['latin_verbs', 'latin_nouns', 'latin_translations', 'latin_words_translations_mappings', 'words',
                        'latin_adverbs', 'latin_prepositions', 'latin_conjunctions', 'latin_pronouns',
                        'latin_adjectives', 'translation_results']

if __name__ == '__main__':
    engine = create_engine('sqlite:///lang_learning.sqlite')

    # begin() means autocommit at the end of the block
    with engine.begin() as conn:
        for t in tables_to_be_cleaned:
            conn.execute(text(f"""delete from {t}"""))
