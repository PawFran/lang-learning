#!/usr/bin/env python

from langchain_openai import ChatOpenAI
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise Exception('must give at least one word')

    llm = ChatOpenAI()

    prompt = ' '.join(sys.argv[1:])

    response = llm.invoke(prompt)

    print(response.content)
