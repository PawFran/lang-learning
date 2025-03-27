from abc import ABC, abstractmethod
from datetime import datetime as dt

import pandas as pd

datetime_format = '%Y-%m-%d %H:%M:%S'
separator = ';'


def human_readable_sets(s):
    return str(sorted(s)).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('\'', '')


class ExerciseCSVHandler(ABC):
    def __init__(self, path, user_name):
        """
        Abstract base class enforcing that subclasses must define how
        current_session_id is stored and retrieved, but providing a
        shared method for determining the session ID from the CSV.
        """
        self.path = path
        self.user_name = user_name

    @property
    @abstractmethod
    def current_session_id(self):
        """
        Subclasses must implement a getter for current_session_id.
        """
        pass

    @current_session_id.setter
    @abstractmethod
    def current_session_id(self, value):
        """
        Subclasses must implement a setter for current_session_id.
        """
        pass

    def get(self):
        return pd.read_csv(self.path, sep=separator, parse_dates=['time'], date_format=datetime_format)

    def create_new_session_id(self):
        """
        Create session id for current session
        """
        df = pd.read_csv(self.path, sep=separator, usecols=['user', 'session_id'])
        user_sessions = df.query('user == @self.user_name').session_id
        if user_sessions.empty:
            return 1
        else:
            return user_sessions.max() + 1


class DeclensionExerciseCSVHandler(ExerciseCSVHandler):
    def __init__(self, path, user_name):
        super().__init__(path, user_name)
        self._current_session_id = self.create_new_session_id()

    @property
    def current_session_id(self):
        return self._current_session_id

    @current_session_id.setter
    def current_session_id(self, value):
        self._current_session_id = value

    def update_db(self, user, lang: str, base_word: str, number: str, case: str, correct_form: str, user_answer: str,
                  is_correct: bool):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, user, lang, base_word, number, case, correct_form, user_answer, is_correct)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df, user, lang, base_word, number, case, correct_form, user_answer, is_correct):
        new_row = pd.DataFrame({'user': user,
                                'session_id': self.current_session_id,
                                'lang': lang,
                                'base_word': base_word,
                                'number': number,
                                'case': case,
                                'correct_form': correct_form,
                                'user_answer': user_answer,
                                'is_correct': is_correct,
                                'time': dt.now().replace(microsecond=0)
                                }, index=[0])
        return pd.concat([df, new_row])


class DeclensionExerciseSessionMetadataCSVHandler:
    def __init__(self, path: str, session_id: int, user_name: str, declensions_included: {str}):
        self.path = path
        self.session_id = session_id
        self.user_name = user_name
        self.declensions_included = declensions_included

    def update(self, interrupted: bool):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, interrupted)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df, interrupted: bool):
        new_row = pd.DataFrame({
            'session_id': self.session_id,
            'user_name': self.user_name,
            'declensions_included': human_readable_sets(self.declensions_included),
            'interrupted': interrupted
        }, index=[0])
        return pd.concat([df, new_row])


class ConjugationExerciseSessionMetadataCSVHandler:
    def __init__(self, path: str, session_id: int, user_name: str, conjugations_included: {str}, moods_included: {str},
                 tenses_included: {str}, voices_included: {str}):
        self.path = path
        self.session_id = session_id
        self.user_name = user_name
        self.conjugations_included = conjugations_included
        self.moods_included = moods_included
        self.tenses_included = tenses_included
        self.voices_included = voices_included

    def update(self, interrupted: bool):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, interrupted)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df, interrupted: bool):
        new_row = pd.DataFrame({'session_id': self.session_id,
                                'user_name': self.user_name,
                                'conjugations_included': human_readable_sets(self.conjugations_included),
                                'moods_included': human_readable_sets(self.moods_included),
                                'tenses_included': human_readable_sets(self.tenses_included),
                                'voices_included': human_readable_sets(self.voices_included),
                                'interrupted': interrupted
                                }, index=[0])
        return pd.concat([df, new_row])


class TranslationExerciseSessionMetadataCSVHandler:
    def __init__(self, path: str, session_id: int, user_name: str, revise_last_session: bool, start_word: str | None,
                 end_word: str | None, filtered_parts_of_speech: {str}):
        self.path = path
        self.session_id = session_id
        self.user_name = user_name
        self.revise_last_session = revise_last_session
        self.start_word = start_word
        self.end_word = end_word
        self.filtered_parts_of_speech = filtered_parts_of_speech

    def update(self, interrupted: bool):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, interrupted)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df, interrupted: bool):
        new_row = pd.DataFrame({
            'session_id': self.session_id,
            'user_name': self.user_name,
            'revise_last_session': self.revise_last_session,
            'start_word': self.start_word if self.start_word is not None else '',
            'end_word': self.end_word if self.end_word is not None else '',
            'filtered_parts_of_speech': human_readable_sets(
                self.filtered_parts_of_speech) if self.filtered_parts_of_speech is not None else '',
            'interrupted': interrupted
        }, index=[0])
        return pd.concat([df, new_row])


class ConjugationExerciseCSVHandler(ExerciseCSVHandler):
    def __init__(self, path, user_name):
        super().__init__(path, user_name)
        self._current_session_id = self.create_new_session_id()

    @property
    def current_session_id(self):
        return self._current_session_id

    @current_session_id.setter
    def current_session_id(self, value):
        self._current_session_id = value

    def update_db(self, user, lang, infinitive, mood, tense, voice, person, number, correct_form, user_answer,
                  is_correct):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, user, lang, infinitive, mood, tense, voice, person, number, correct_form,
                                 user_answer, is_correct)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df, user, lang, infinitive, mood, tense, voice, person, number, correct_form, user_answer,
                       is_correct):
        new_row = pd.DataFrame({'user': user,
                                'session_id': self.current_session_id,
                                'lang': lang,
                                'infinitive': infinitive,
                                'mood': mood,
                                'tense': tense,
                                'voice': voice,
                                'person': person,
                                'number': number,
                                'correct_form': correct_form,
                                'user_answer': user_answer,
                                'is_correct': is_correct,
                                'time': dt.now().replace(microsecond=0)
                                }, index=[0])
        return pd.concat([df, new_row])


class TranslationExerciseCSVHandler(ExerciseCSVHandler):
    def __init__(self, path, user_name):
        super().__init__(path, user_name)
        self._current_session_id = self.create_new_session_id()

    @property
    def current_session_id(self):
        return self._current_session_id

    @current_session_id.setter
    def current_session_id(self, value):
        self._current_session_id = value

    def update_db(self, user: str, word_pl: str, lang: str, translation: str, was_correct: bool, user_answer: str):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, lang, translation, user, was_correct, word_pl, user_answer)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df, lang, translation, user, was_correct, word_pl, user_answer):
        new_row = pd.DataFrame({'user': user,
                                'session_id': self.current_session_id,
                                'lang': lang,
                                'word_pl': word_pl,
                                'correct_translation': translation,
                                'user_answer': user_answer,
                                'is_correct': was_correct,
                                'time': dt.now().replace(microsecond=0)
                                }, index=[0])
        return pd.concat([df, new_row])


class ReversedTranslationExerciseCSVHandler(ExerciseCSVHandler):
    def __init__(self, path, user_name, lang: str):
        super().__init__(path, user_name)
        self._current_session_id = self.create_new_session_id()
        self.lang = lang

    @property
    def current_session_id(self):
        return self._current_session_id

    @current_session_id.setter
    def current_session_id(self, value):
        self._current_session_id = value

    def update_db(self, head_raw: str, example: str,
                  number_of_translations_total: int, translations_left: list[str],
                  user_answer: str, was_correct: bool):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, head_raw, example,
                                 number_of_translations_total, translations_left,
                                 user_answer, was_correct)

        df.to_csv(self.path, index=False, sep=';')

    def add_new_record(self, df: pd.DataFrame,
                       head_raw: str, example: str,
                       number_of_translations_total: int, translations_left: list[str],
                       user_answer: str, was_correct: bool):
        new_row = pd.DataFrame({'user': self.user_name,
                                'session_id': self.current_session_id,
                                'lang': self.lang,
                                'word_asked': head_raw,
                                'example': example,
                                'translations_total_nr': number_of_translations_total,
                                'translations_left': "\n".join(translations_left),
                                'user_answer': user_answer,
                                'is_correct': was_correct,
                                'time': dt.now().replace(microsecond=0)
                                }, index=[0])
        return pd.concat([df, new_row])
