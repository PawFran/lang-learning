#!/usr/bin/env python

import os
import re
import sys

from openai import OpenAI

from utils.lib.utils import process_text

this_script_path = os.path.dirname(__file__)
output_temporary_file = os.path.join(this_script_path, 'scraping_out_tmp.txt')


def llm_explain_word_dict_format(word: str, llm, f, sentence: str = None, context: str = None):
    prompt = f'''
        explain word "{word}" using Cambridge Dictionary in the following format:
        word [part of speech]
        ()
        1. explanation
        (if there is more than one explanation you can list them using subsequent numbers)

        I will give you some example for word \'battered\':
        battered [adjective]
        ()
        1. hurt by being repeatedly hit
        2. damaged, especially by being used a lot

        If You cannot find word please tell me that i probably made mistake and don't try to forcefully come up with something. 
        You may give me instead suggestions with similar words in case I just misspelled it. 
        For example if i write word \'beffled\' You can respond:
        Cannot find \'beffled\' but I have found word(s) with similar spelling:
        1. baffled
        '''

    completion = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response = completion.choices[0].message.content

    if sentence is not None:
        response = fill_response_with_example(response, sentence)

    if context is not None:
        response = add_context_to_response(response, context)

    # remove dot at avery line if exists
    response = re.sub(r"\.\s*$", "", response, flags=re.MULTILINE) + '\n'

    print(response)
    f.write(response + '\n')


def add_context_to_response(txt, context) -> str:
    split = txt.split('\n')
    split[1] = f'{split[1].strip()} [{context}]'

    return '\n'.join(split)


def fill_response_with_example(txt, sentence):
    split = txt.split('\n')
    split[1] = split[1].replace('()', f'({sentence})')

    return '\n'.join(split)


if __name__ == '__main__':
    # Read input from command line arguments
    if len(sys.argv) < 2:
        print(
            "Usage: python test_english.py words separated by space (sentence optionally with some words surrounded by \\) [context]")
        sys.exit(1)

    input_text = sys.argv[1]
    words, example, context = process_text(input_text)

    llm = OpenAI()

    with (open(output_temporary_file, 'a', encoding="utf-8") as f):
        for input_word in words:
            llm_explain_word_dict_format(input_word, llm, f, sentence=example, context=context)

    # TODO first try to find if the word is already present
