import speech_recognition as sr


def capture_voice_input(recognizer):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio


def convert_voice_to_text(audio, recognizer):
    try:
        text = recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.\n")
    except sr.RequestError as e:
        text = ""
        print(f"Error; {e}\n")
    return text


def ask_llm(text, llm):
    response = llm.invoke(text).content
    return response


def test_convert_voice_to_text(audio, recognizer):
    try:
        text = recognizer.recognize_google(audio)

        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Sorry, I didn't understand that.")
    except sr.RequestError as e:
        text = ""
        print("Error; {0}".format(e))
    return text


def process_voice_command(text):
    if "hello" in text.lower():
        print("Hello! How can I help you?")
    elif "goodbye" in text.lower():
        print("Goodbye! Have a great day!")
        return True
    else:
        print("I didn't understand that command. Please try again.")
    return False
