from sqlalchemy import create_engine

from database.utils import *


def migrate_dictionary(engine, dict_folder):
    args = parse_args()

    args.language = 'latin'

    dictionary: Dictionary = parse_dictionary(args, dictionary_folder=dict_folder)

    add_words_with_translations(dictionary, engine)


def add_words_with_translations(dictionary, engine):
    words_not_added = 0
    with Session(engine) as session:
        for entry in dictionary.entries:
            head = entry.head
            if type(head) is LatinVerb:
                insert_or_ignore_latin_word(entry, verb_from_head, session)
            elif type(head) is LatinNoun:
                insert_or_ignore_latin_word(entry, noun_from_head, session)
            elif type(head) is LatinAdverb:
                insert_or_ignore_latin_word(entry, adverb_from_head, session)
            elif type(head) is LatinPreposition:
                insert_or_ignore_latin_word(entry, preposition_from_head, session)
            elif type(head) is LatinConjunction:
                insert_or_ignore_latin_word(entry, conjunction_from_head, session)
            elif type(head) is LatinPronoun:
                insert_or_ignore_latin_word(entry, pronoun_from_head, session)
            elif type(head) is LatinAdjective:
                insert_or_ignore_latin_word(entry, adjective_from_head, session)
            else:
                print(f'{entry.head.base} not added')
                words_not_added += 1
    if words_not_added > 0:
        print(f'\n{words_not_added} words were not tried to be added')


if __name__ == '__main__':
    engine = create_engine(DATABASE)
    dict_folder = os.path.join('..', 'vocabulary', 'dicts')
    migrate_dictionary(engine, dict_folder)
