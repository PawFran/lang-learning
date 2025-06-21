# Lang-Learning

A collection of modules for language learning. 

## Setup
For this app to work one must edit .env_template file (in environment dir):
* fill all values (ex. DATABASE_URL)
* change name to .env

## Modules

- **Vocabulary**: Learn and review vocabulary.
- **Latin Grammar**: Study Latin grammar patterns (conjugations, declensions, etc.).
- **Resources**: Contains key mappings for Sublime Text 3 to type characters with accents.

## Tools

- **Testing**: Use `pytest` for unit testing.
- **Type Validation**: Use `mypy` for type checking.

---

## Lang learning web app

### Usage
```bash
python app.py
```
**Important** for correct working one must specify environment variables in ```.env``` file (top level directory): 
- DATABASE_URL

## Random Word from Dictionary

This tool displays random words with translations for vocabulary practice. It's read-only and does not require user input.

### Usage
```bash
python random_word.py -h           # Help
python random_word.py -l LANGUAGE  # Choose language (english or latin - required)
```

#### Additional Flags
- **-r / --remove**: Option to hide words after they appear (for the current session).
- **-a and -z**: Define a subset range by starting and ending words (inclusive).
- **-u**: (Currently not in use) Will support user-specific learning data for tracking in the future.
- **Expressions**: Use quotes for multi-word expressions.
- **Error Handling**: Ensure both words in range exist in the dictionary; otherwise, an error will occur.

---

## Translation Exercise

A guessing game that displays a Polish word and asks for the translation.

### Usage
```bash
python translation_exercise.py
```

#### Flags and Options
- **-k**: Keeps words even after a correct answer.
- **-f**: Filter entries with multiple criteria. Separate filters with spaces and use a pipe (\`|\`) for "OR" conditions.
  - Example: \`-f verb II | noun I II | adj\` filters for verbs (2nd conj.), nouns (1st or 2nd declension), and adjectives.
- **Special Cases**:
  - **Verbs (1st conj.)**: Answer can be "base āre āvi ātum" or "base 1".
  - **Adjectives (1st/2nd conj.)**: Answer can be "base a um".

With a user profile set up, "smart sampling" gives priority to:
  - New words
  - Incorrectly guessed words (last 3 trials)
  - Words not seen recently

---

## Declension Practice

### Usage
```bash
python declension_exercise.py -d DECLENSIONS -w WORDS -k (optional)
```

For easier access, add this alias to your `~/.zshrc` file:
```bash
alias declension='python /full/path/to/declension_exercise.py'
```

Then you can simply use:
```bash
declension -d 1 2 demonstrative -w hic haec hoc 
```

#### Declensions
Specify declensions as a list:
- Options: \`1, 2, 3, "3 consonant", "3 vowel", "3 mixed", 4, 5, relative, interrogative, demonstrative\`
- Words or numbers are allowed, and underscores (\`_\`) or hyphens (e\`-\`) can replace spaces.
- when both "d" and "w" options are specified it is understood than they are to be used in together like with "&" operator

---

## Conjugation Practice

### Usage
```bash
python conjugation_exercise.py -c CONJUGATIONS -m MOODS -v VOICES -t TENSES -k
```

For easier access, add this alias to your `~/.zshrc` file:
```bash
alias conjugation='python /full/path/to/conjugation_exercise.py'
```

Then you can simply use:
```bash
conjugation -c 1 2 -m indicative -v active -t present -k
```

#### Options
Separate multiple conjugations, moods, voices, or tenses by spaces.

---

## Scraping Latin Dictionary

Scrape Latin dictionary entries for specified words.

### Usage
```bash
python scrape_latin_dict.py [list of words separated by spaces]
```

---

## Find or Scrape

Looks for specified words in the database; if not found, it initiates a scrape.

### Usage
```bash
python find_or_scrape.py [list of words to be found]
```

- **Output**: Found words are printed under the "found" hashtag; others are scraped.

---

## English Dictionary

Look up English words with their definitions and example sentences.

### Usage
```bash
python english.py "words separated by space (sentence optionally with some words surrounded by \) [context]"
```

Examples:
```bash
# Single word
python english.py spotty

# Multiple words
python english.py spotty harness

# Word included in example and context
python english.py "(Thanks to the wifi... which is \spotty\ at best) [The simpsons - Lisa]"

# Word outside with example and context
python english.py "spotty (Thanks to the wifi... which is spotty at best) [The simpsons - Lisa]"
```

---

## Other info
DB documentation:
* https://dbdiagram.io/d/lang-learning-6739c159e9daa85acab7031e
* https://dbdocs.io/pawel.fran/lang-learning?schema=public&view=relationships&table=latin_verbs
