#!/usr/bin/env python

import sys

from openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate

output_temporary_file_name = 'scraping_out_tmp.txt'


def llm_explain_word_dict_format(word, llm, f, sentence=None):
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

    response = completion.choices[0].message.content + '\n'
    if sentence is not None:
        response = fill_response_with_example(response, sentence)
    print(response)
    f.write(response + '\n')


def fill_response_with_example(txt, sentence):
    split = txt.split('\n')
    split[1] = f'({sentence})'

    return '\n'.join(split)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('must give at least one argument (word to be found)')

    # TODO first try to find if the word is already present

    llm = OpenAI()

    # print('\n')

    with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
        for input_word in sys.argv[1:]:
            llm_explain_word_dict_format(input_word, llm, f)
