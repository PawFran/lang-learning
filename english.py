#!/usr/bin/env python

from langchain_openai import ChatOpenAI
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('must give at least one argument (word to be found)')

    llm = ChatOpenAI()

    output_temporary_file_name = 'scraping_out_tmp.txt'

    print('\n')

    with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
        for input_word in sys.argv[1:]:
            response = llm.invoke(
                f'''explain word "{input_word}" using Cambridge Dictionary in the following format:
                word [part of speech]
                ()
                1. explanation
                ( if there is more than one explanation you can list them using subsequent numbers)
    
                I will give you some example for word \'battered\':
                battered [adjective]
                ()
                1. hurt by being repeatedly hit
                2. damaged, especially by being used a lot
                '''
            ).content + '\n'

            print(response)
            f.write(response + '\n')
