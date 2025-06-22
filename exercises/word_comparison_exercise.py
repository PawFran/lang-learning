import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import any_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression

from database.db_classes import Words
from environment.setup import engine

WORD_COMPARISON_PATH = os.path.join(os.path.dirname(__file__), 'vocabulary', 'dicts', 'word_comparison.txt')


def clean_words(lines_raw):
    words_split = [line.split('vs') for line in lines_raw]
    return [list(map(str.strip, words_set)) for words_set in words_split]


def flatten_pairs(pairs: list[list[str]]) -> list[str]:
    return [word for pair in pairs for word in pair]


def get_matching_words_from_db(words_of_interest: list[str]) -> list[type[Words]]:
    # TODO more exact matching not substring & replace special chars in both words_of_interest and words in db
    condition: BinaryExpression = Words.header.like(any_([f"%{word}%" for word in words_of_interest]))
    with Session() as session:
        db_words: list[type[Words]] = session.query(Words).filter(condition).all()

    return db_words


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)

    with open(WORD_COMPARISON_PATH) as f:
        word_comparison_lines_raw = [line.strip() for line in f.readlines()]

    pairs_to_compare = clean_words(word_comparison_lines_raw)
    words_to_compare = flatten_pairs(pairs_to_compare)

    db_words = get_matching_words_from_db(words_to_compare)

    print([w.header for w in db_words])
