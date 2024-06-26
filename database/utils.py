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


def insert_or_ignore(session, record):
    try:
        session.add(record)
        session.flush()
    except IntegrityError:
        print(f'integrity error during upsert of {record}')
        session.rollback()


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

    except Exception as e:
        session.rollback()
        print("Error:", str(e))
