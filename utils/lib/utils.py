import re

def print_all(lst):
    for i in range(len(lst)):
        print(f'{i + 1}. {lst[i]}')


def answer_split(answer: str) -> list[str]:
    return [x for x in answer.split(' ') if x != '']


def is_proper_answer(answer: str) -> bool:
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
