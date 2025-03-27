import re

def print_all(lst):
    for i in range(len(lst)):
        print(f'{i + 1}. {lst[i]}')
    

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
