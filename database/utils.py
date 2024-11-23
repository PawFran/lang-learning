from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from common.lib.utils import replace_special
from database.db_classes import *
from vocabulary.lib.parsing_dict import *


def verb_from_head(word_id, head):
    return LatinVerbs(id=word_id,
                      base_word=replace_special(head.base),
                      base_word_acc=head.base,
                      infinite=replace_special(head.infinite),
                      infinite_acc=head.infinite,
                      perfect=replace_special(head.perfect),
                      perfect_acc=head.perfect,
                      supine=replace_special(head.supine),
                      supine_acc=head.supine,
                      additional_info=None,
                      conjugation=head.conjugation.name)


def noun_from_head(word_id, head):
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

    return LatinNouns(id=word_id,
                      base=replace_special(head.base),
                      base_acc=head.base,
                      gen=replace_special(head.genetive),
                      gen_acc=head.genetive,
                      declension=head.declension,
                      genre=genre,
                      only_pl='true' if head.only_plural else 'false')


def adverb_from_head(word_id, head):
    return LatinAdverbs(id=word_id,
                        base=replace_special(head.base),
                        base_acc=head.base)


def preposition_from_head(word_id, head):
    return LatinPrepositions(id=word_id,
                             base=replace_special(head.base),
                             base_acc=head.base)


def conjunction_from_head(word_id, head):
    return LatinConjunctions(id=word_id,
                             base=replace_special(head.base),
                             base_acc=head.base)


def pronoun_from_head(word_id, head):
    return LatinPronouns(id=word_id,
                         base=replace_special(head.base),
                         base_acc=head.base)


def adjective_from_head(word_id, head):
    return LatinAdjectives(id=word_id,
                           base=replace_special(head.base),
                           base_acc=head.base)


def insert_or_ignore(session: Session, record):
    session.add(record)
    session.flush()


def insert_or_ignore_latin_word(entry: DictionaryEntry, parsing_function, session: Session):

    try:
        head = entry.head
        head_raw = head.head_raw
        part_of_speech = head.part_of_speech().value

        # Insert into "words" table
        word = Words(lang="latin", header=head_raw, part_of_speech=part_of_speech)
        insert_or_ignore(session, word)

        word_id = session.query(Words).filter_by(header=head_raw).first().id

        # Insert into "latin_translations" table
        translation_ids = insert_and_get_translation_ids(entry, session)

        # Upsert word into appropriate table (ex. LatinVerbs)
        word = parsing_function(word_id, head)
        insert_or_ignore(session, word)

        # Get info about upsert word to fill related tables
        # part_of_speech, word_id = get_part_of_speech_and_word_id(head, session, word)

        # Commit changes to the session before retrieving translation IDs
        session.commit()

        insert_word_translation_mappings(word_id=word_id, part_of_speech=part_of_speech, session=session,
                                         translation_ids=translation_ids)

        session.commit()

    except IntegrityError as e:
        print(f'integrity error during upsert of {head.base}: {e}')
        session.rollback()
    except Exception as e:
        session.rollback()
        print(f"Error - {head.base} not migrated because of:", str(e))


def get_part_of_speech_and_word_id(head, session, word):
    word_id = None
    part_of_speech = None
    if type(head) is LatinVerb:
        word_id = session.query(LatinVerbs).filter_by(base_word_acc=word.base_word_acc).first().id
        part_of_speech = 'verb'
    elif type(head) is LatinNoun:
        word_id = session.query(LatinNouns).filter_by(base=word.base, gen=word.gen).first().id
        part_of_speech = 'noun'
    elif type(head) is LatinAdverb:
        word_id = session.query(LatinAdverbs).filter_by(base_acc=word.base_acc).first().id
        part_of_speech = 'adverb'
    elif type(head) is LatinPreposition:
        word_id = session.query(LatinPrepositions).filter_by(base_acc=word.base_acc).first().id
        part_of_speech = 'preposition'
    elif type(head) is LatinConjunction:
        word_id = session.query(LatinConjunctions).filter_by(base_acc=word.base_acc).first().id
        part_of_speech = 'conjunction'
    elif type(head) is LatinPronoun:
        word_id = session.query(LatinPronouns).filter_by(base_acc=word.base_acc).first().id
        part_of_speech = 'pronoun'
    elif type(head) is LatinAdjective:
        word_id = session.query(LatinAdjectives).filter_by(base_acc=word.base_acc).first().id
        part_of_speech = 'adjective'
    return part_of_speech, word_id


def insert_word_translation_mappings(word_id, part_of_speech, session, translation_ids):
    # Retrieve translation IDs from the list
    for translation_id in translation_ids:
        # For each verb-translation pair, upsert appropriate record into mapping table
        mapping = LatinWordsTranslationsMappings(word_id=word_id, translation_id=translation_id,
                                                part_of_speech=part_of_speech)
        insert_or_ignore(session, mapping)


def insert_and_get_translation_ids(entry, session):
    translation_ids = []
    for t in entry.translations:
        # For each translation, upsert it
        is_already_present = session.query(LatinTranslations).filter_by(text=t).count() > 0
        # print(is_already_present)
        if not is_already_present:
            translation = LatinTranslations(text=t, example=entry.example, associated_case=None)
            insert_or_ignore(session, translation)

            # Append the translation ID to the list
            translation_ids.append(session.query(LatinTranslations).filter_by(text=t).first().id)
    return translation_ids
