from database.utils import *

if __name__ == '__main__':
    args = parse_args()

    args.language = 'latin'

    dict_folder = os.path.join('..', 'vocabulary', 'dicts')
    dictionary: Dictionary = parse_dictionary(args, dictionary_folder=dict_folder)

    with Session(engine) as session:
        for entry in dictionary.entries:
            head = entry.head
            if type(head) is LatinVerb:
                upsert_latin_verb(entry, session)
            # elif type(head) is LatinNoun:
            #
            else:
                print(f'{entry.head.base} not migrated')
