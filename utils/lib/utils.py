import re

from synonyms.utils import SynonymWithScore


def print_all(lst: list[str]):
    for i in range(len(lst)):
        print(f'{i + 1}. {lst[i]}')


def print_all_synonyms(lst: list[SynonymWithScore]):
    for i in range(len(lst)):
        current = lst[i]
        print(f'{i + 1}. {current.synonym} ({100*round(current.score, 2)}%)')


def answer_split(answer: str) -> list[str]:
    return [x for x in answer.split(' ') if x != '']


def only_digits(answer: str) -> bool:
    return all([x.isdigit() for x in answer_split(answer)])


def answer_parsed(answer: str) -> list[int]:
    return [int(x) for x in answer_split(answer)]
    

def process_text(text):
    # Extract words outside of any brackets
    text_outside_brackets = re.sub(r'\(.*?\)|\[.*?\]', '', text)  # Remove content inside () and []
    words = set(re.findall(r'\b\w+\b', text_outside_brackets))  # Extract standalone words

    # Extract ALL words within square brackets that are surrounded by "\"
    words_in_brackets = re.findall(r'\\(\w+)\\', text)
    words.update(words_in_brackets)  # Add them to the set

    # Extract example sentence inside parentheses, removing "\"
    example_match = re.search(r'\((.*?)\)', text)
    example = example_match.group(1).replace("\\", "") if example_match else ""

    # Extract context within square brackets and remove "\" inside it
    context_match = re.search(r'\[(.*?)\]', text)
    context = context_match.group(1).replace("\\", "") if context_match else ""

    return words, example, context
