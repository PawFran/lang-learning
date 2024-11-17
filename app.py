from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from find_or_scrape_latin import find_or_scrape_words, SCRAPED_HEADER, find_or_scrape_sentence

from vocabulary.lib.parsing_dict import parse_latin_dict
from vocabulary.lib.utils import DICT_DIR_PATH

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start_translation_session', methods=['POST'])
def start_translation_session():
    data = request.get_json()
    start = data['start'].strip()
    end = data['end'].strip()
    response_text = f"Starting session with start word {start} end word {end}"
    print(response_text)
    return jsonify({'response': response_text})


@app.route('/finish_translation_session', methods=['POST'])
def finish_translation_session():
    response_text = f"Session finished"
    return jsonify({'response': response_text})


@app.route('/translation', methods=['POST'])
def check_translation():
    data = request.get_json()
    word = data['word']
    translation = data['translation']
    response_text = f"System will check if {translation} is correct translation for {word}"
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

    response_text = find_or_scrape_words(words, example = sentence)

    return jsonify({'response': response_text})


@app.route('/dictionary', methods=['POST'])
def add_to_dict():
    data = request.get_json()
    raw_lines = data['data']
    lines = [l + '\n' for l in raw_lines.split('\n') if l != '\n'] # to quickly reuse parsing function for files newline character must be preserved
    start_from = lines.index(SCRAPED_HEADER) + 1 if SCRAPED_HEADER in lines else 0
    lines_to_be_parsed = lines[start_from:]

    dict_to_be_added = parse_latin_dict(lines_to_be_parsed)
    result = dict_to_be_added.save_to_file(DICT_DIR_PATH)

    response_text = f'added to text dict:\n{result}'
    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(debug=True)
