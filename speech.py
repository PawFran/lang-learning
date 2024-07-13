from speech.utils import *
from langchain_openai import ChatOpenAI
import re
from english import output_temporary_file_name, llm_explain_word_dict_format

translation_pattern = 'translate (.*) in (.*)'

if __name__ == "__main__":
    llm = ChatOpenAI()

    recognizer = sr.Recognizer()

    end_program = False
    while not end_program:
        audio = capture_voice_input(recognizer)

        text = convert_voice_to_text(audio, recognizer)
        if text != "":
            print("You said: " + text)

            try:
                groups = re.search(pattern=translation_pattern, string=text).groups()
                if groups is not None:
                    word = groups[0]
                    sentence = groups[1].capitalize()

                    with (open(output_temporary_file_name, 'a', encoding="utf-8") as f):
                        llm_explain_word_dict_format(word, llm, f, sentence)
            except:
                print(f'couldn\'t match pattern: {translation_pattern}')

        end_program = process_voice_command(text)
