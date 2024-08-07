from database.utils import *

if __name__ == '__main__':
    args = parse_args()

    args.language = 'latin'

    dict_folder = os.path.join('..', 'vocabulary', 'dicts')
    dictionary: Dictionary = parse_dictionary(args, dictionary_folder=dict_folder)

    words_not_migrated = 0

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
                print(f'{entry.head.base} not migrated')
                words_not_migrated += 1

    print(f'\n{words_not_migrated} words not migrated')
