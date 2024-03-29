from datetime import datetime as dt

import pandas as pd

datetime_format = '%Y-%m-%d %H:%M:%S'
separator = ';'


class TranslationExerciseDBHandler:
    def __init__(self, path, user_name):
        self.path = path
        self.current_session_id = TranslationExerciseDBHandler.get_current_user_session_id(self.path, user_name) + 1

    @staticmethod
    def get_current_user_session_id(path, user_name):
        return pd.read_csv(path, sep=separator, usecols=['user', 'session_id']) \
            .query('user == @user_name').session_id.values.max()

    def get(self):
        return pd.read_csv(self.path, sep=separator, parse_dates=['time'], date_format=datetime_format)

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
