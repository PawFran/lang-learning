import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import create_engine

from actions.translation import *
from database.db_classes import DB_FILE_NAME
from database.initialize_db import initialize_database
from database.migration_dictionary import add_words_with_translations
from find_or_scrape_latin import find_or_scrape_words, SCRAPED_HEADER
from vocabulary.lib.dict_classes import Dictionary
from vocabulary.lib.parsing_dict import parse_latin_dict
from vocabulary.lib.utils import DICT_DIR_PATH

app = Flask(__name__)
CORS(app)

DB_DIR = 'database'
DB_PATH = os.path.join(DB_DIR, DB_FILE_NAME)
DATABASE = f'sqlite:///{DB_PATH}'
engine = create_engine(DATABASE)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start_translation_session', methods=['POST'])
def start_translation_session():
    data = request.get_json()
    start = data['start'].strip()
    end = data['end'].strip()
    with Session(engine) as session:
        words_cnt = start_translation_exercise_session(start_word=start, end_word=end, session=session)
        if words_cnt > 0:
            word = random_word_for_cache(session)
            response_text = f"Starting session with start word: \"{start}\" and end word: \"{end}\". Number of words: {words_cnt}\n\n{word}"
        else:
            response_text = f"Trying to start session with start word: \"{start}\" and end word: \"{end}\" - but no words found!"
    print(response_text)
    return jsonify({'response': response_text})


@app.route('/finish_translation_session', methods=['POST'])
def finish_translation_session():
    # todo clear cache
    response_text = f"Session finished"
    return jsonify({'response': response_text})


@app.route('/translation', methods=['POST'])
def check_translation():
    data = request.get_json()
    answer = data['answer']
    with Session(engine) as session:
        feedback: TranslationFeedback = check_translation_answer(answer, session)
        if feedback.is_correct:
            remove_from_cache(feedback.word_id, session)
        new_word = random_word_for_cache(session)

    response_text = f'{answer}\n'

    if feedback.is_correct:
        response_text += f"correct "
    else:
        response_text += f"wrong. correct answer is \"{feedback.correct_answer}\""

    if feedback.example is not None and feedback.example != '':
        response_text += f'({feedback.example})\n'

    # TODO zalogowanie odpowiedzi. wpisanie rezultatu na bazę i do pliku

    if new_word is None:
        response_text += 'no more words for this session'
        # todo trigger finish ? maybe it should be structured differently
        # todo response should be divided between feedback and info about next word (or finish)
        # todo and appropriate logic should be applied on the client side
    else:
        response_text += f'\n\n{new_word}'

    return jsonify({'response': response_text})


@app.route('/start_declension_session', methods=['POST'])
def start_declension_session():
    data = request.get_json()  # Get the JSON data sent by the client
    declensions = data['declensions']
    print("Received declensions:", declensions)  # Log the declensions to the console

    # Send back a confirmation response
    return jsonify({'status': 'success', 'received': declensions})


@app.route('/finish_declension_session', methods=['POST'])
def finish_declension_session():
    response_text = f"Session finished"
    return jsonify({'response': response_text})


@app.route('/declension_answer', methods=['POST'])
def check_declension_answer():
    data = request.get_json()
    word = data['word']
    answer = data['answer']
    response_text = f"System will check if {answer} is correct"
    return jsonify({'response': response_text})


@app.route('/start_conjugation_session', methods=['POST'])
def start_conjugation_session():
    data = request.get_json()  # Get the JSON data sent by the client
    conjugations = data['conjugations']
    moods = data['moods']
    voices = data['voices']
    tenses = data['tenses']

    # Send back a confirmation response
    return jsonify({'status': 'success', 'received': conjugations})


@app.route('/finish_conjugation_session', methods=['POST'])
def finish_conjugation_session():
    response_text = f"Session finished"
    return jsonify({'response': response_text})


@app.route('/conjugation_answer', methods=['POST'])
def check_conjugation_answer():
    data = request.get_json()
    word = data['word']
    answer = data['answer']
    response_text = f"System will check if {answer} is correct"
    return jsonify({'response': response_text})


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    words_raw = data['words']
    sentence = data['sentence']

    # if no words are specified it means that every word in a sentence must be scraped
    words = [w for w in words_raw.split(' ') if w != '']
    if len(words) == 0:
        words = [w for w in sentence.split(' ') if w != '']

    response_text = find_or_scrape_words(words, example=sentence)
    return jsonify({'response': response_text})


@app.route('/dictionary', methods=['POST'])
def add_to_dict():
    data = request.get_json()
    raw_lines = data['data'].rstrip() + '\n'
    lines = [l + '\n' for l in raw_lines.split('\n') if
             l != '\n']  # to quickly reuse parsing function for files newline character must be preserved
    start_from = lines.index(SCRAPED_HEADER) + 2 if SCRAPED_HEADER in lines else 0
    lines_to_be_parsed = lines[start_from:]

    dict_to_be_added: Dictionary = parse_latin_dict(lines_to_be_parsed)

    add_words_with_translations(dict_to_be_added, engine)
    saved_to_file = dict_to_be_added.save_to_file(DICT_DIR_PATH)

    response_text = f'saved to file: {saved_to_file}'
    return jsonify({'response': response_text})


if __name__ == '__main__':
    # Flask's development server uses a reloading mechanism.
    # This mechanism starts a child process to handle the actual running of the server,
    # which causes the __main__ block to execute twice: once in the parent process and once in the child process.
    # this if is to assure it will be run once
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # This block will only be executed in the child process
        print('initializing db')
        dict_folder = os.path.join('vocabulary', 'dicts')
        translation_results_dir = os.path.join('vocabulary', 'db')
        initialize_database(db_path=DB_PATH, remove_old=True, dictionary_migration=True,
                            translation_results_migration=True,
                            dictionary_folder=dict_folder, translation_results_folder=translation_results_dir)
    app.run(debug=True)
