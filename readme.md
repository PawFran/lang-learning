# lang-learning

## collection of modules related with languages learning (more info in readme's of each module)

### vocabulary module is dedicated to learning vocabulary

### latin_grammar module is for learning grammatical patterns of latin (conjugations, declensions etc.)

### ./resources catalog contains key mapping for sublime text 3 allowing to type letters with long accent

### use pytest to run unit tests

### use mypy for type validation

# random word from dictionary

### printing random words (no users input, read only for learning - first word, then translation)

## how to use it

### python random_word.py -h (for help)

### python random_word.py -l _language_ (english or latin - mandatory)

### when -r or --remove flag is user may decide whether they want not to see particular word again (current session)

### -a and -z flags are used to subset dictionary using words (start/end) inclusive

### -u flag is useless for now. it makes sense for "translation script" (sets the user to save their results)

### expressions with more than one word must be put in ""

### if one of words is not present in dict or end is before start the will be an error

### random words will appear on the console one by one until user will tell it to stop

# translation

### guessing game - print polish word, then ask for translation and evaluate it

## how to use it

### python translation_exercise.py

### all options are like in _random_word.py_

### in case of -r flag words are removed only after correct answer

### when user is set smart sampling is user (more chances for new words, words which were guessed incorrectly during last 3 trials, words that were asked a long time ago)

# declension

## how to use it

### python declension_exercise.py -d declensions -r (optional)

### where declensions are list of declensions separated by space:

### all possibilities: 1, 2, 3, "3 consonant", "3 vowel", "3 mixed", 4, 5 (also words instead of numbers are possible and _ or - instead of space)

# conjugation

## how to use it

### python conjugation_exercise.py -c conjugations -m moods -v voices -t tenses -r

### multiple conjugations etc. separated by space

# scraping dict

## how to use it

### python scrape_latin_dict.py [list of words separated by spaces]