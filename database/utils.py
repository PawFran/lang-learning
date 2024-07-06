from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.lib.utils import replace_special
from database.db_classes import *
from vocabulary.lib.parsing_dict import *


def verb_from_head(head):
    return LatinVerbs(base_word=replace_special(head.base),
                      base_word_acc=head.base,
                      infinite=replace_special(head.infinite),
                      infinite_acc=head.infinite,
                      perfect=replace_special(head.perfect),
                      perfect_acc=head.perfect,
                      supine=replace_special(head.supine),
                      supine_acc=head.supine,
                      additional_info=None,
                      conjugation=head.conjugation.name)


def noun_from_head(head):
    if head.genre == 'm':
        genre = 'masculine'
    elif head.genre == 'f':
        genre = 'feminine'
    elif head.genre == 'm/f':
        genre = 'masculine and feminine'
    elif head.genre == 'n':
        genre = 'neutral'
    else:
        raise Exception(f'cannot parse {head.genre} to proper genre')

    return LatinNouns(base=replace_special(head.base),
                      base_acc=head.base,
                      gen=replace_special(head.genetive),
                      gen_acc=head.genetive,
                      declension=head.declension,
                      genre=genre,
                      only_pl='true' if head.only_plural else 'false')


def insert_or_ignore(session: Session, record):
    session.add(record)
    session.flush()


def insert_or_ignore_latin_verb(entry: DictionaryEntry, session: Session):
    head = entry.head

    try:
        # Upsert verb and get its id
        verb = verb_from_head(head)
        insert_or_ignore(session, verb)
        verb_id = session.query(LatinVerbs).filter_by(base_word_acc=verb.base_word_acc).first().id

        # Upsert into word table
        word = Words(lang="latin", word_id=verb_id, part_of_speech="verb")
        insert_or_ignore(session, word)

        # List to store translation IDs and mapping IDs
        translation_ids = []

        for t in entry.translations:
            # For each translation, upsert it
            is_already_present = session.query(LatinTranslations).filter_by(text=t)
            # print(is_already_present)
            if is_already_present is None:
                translation = LatinTranslations(text=t, example=entry.example, associated_case=None)
                insert_or_ignore(session, translation)

                # Append the translation ID to the list
                translation_ids.append(session.query(LatinTranslations).filter_by(text=t).first().id)

        # Commit changes to the session before retrieving translation IDs
        session.commit()

        # Retrieve translation IDs from the list
        for translation_id in translation_ids:
            # For each verb-translation pair, upsert appropriate record into mapping table
            mapping = LatinWordsTranslationsMapping(word_id=verb_id, translation_id=translation_id,
                                                    part_of_speech='verb')
            insert_or_ignore(session, mapping)

        session.commit()

    except IntegrityError as e:
        print(f'integrity error during upsert of {head.base}: {e}')
        session.rollback()
    except Exception as e:
        session.rollback()
        print(f"Error - {head.base} not migrated because of:", str(e))


def insert_or_ignore_latin_noun(entry: DictionaryEntry, session: Session):
    head = entry.head

    try:
        # Upsert verb and get its id
        noun = noun_from_head(head)
        insert_or_ignore(session, noun)
        noun_id = session.query(LatinNouns).filter_by(base=noun.base, gen=noun.gen).first().id

        # Upsert into word table
        word = Words(lang="latin", word_id=noun_id, part_of_speech="noun")
        insert_or_ignore(session, word)

        # List to store translation IDs and mapping IDs
        translation_ids = []

        for t in entry.translations:
            # For each translation, upsert it
            is_already_present = session.query(LatinTranslations).filter_by(text=t)
            # print(is_already_present)
            if is_already_present is None:
                translation = LatinTranslations(text=t, example=entry.example, associated_case=None)
                insert_or_ignore(session, translation)

                # Append the translation ID to the list
                translation_ids.append(session.query(LatinTranslations).filter_by(text=t).first().id)

        # Commit changes to the session before retrieving translation IDs
        session.commit()

        # Retrieve translation IDs from the list
        for translation_id in translation_ids:
            # For each verb-translation pair, upsert appropriate record into mapping table
            mapping = LatinWordsTranslationsMapping(word_id=noun_id, translation_id=translation_id,
                                                    part_of_speech='noun')
            insert_or_ignore(session, mapping)

        session.commit()

    except IntegrityError as e:
        print(f'integrity error during upsert of {head.base}: {e}')
        session.rollback()
    except Exception as e:
        session.rollback()
        print(f"Error - {head.base} not migrated because of:", str(e))
