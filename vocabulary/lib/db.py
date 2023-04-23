from datetime import datetime as dt

import pandas as pd

datetime_format = '%Y-%m-%d %H:%M:%S'


class TranslationExerciseDBHandler:
    def __init__(self, path):
        self.path = path

    def get(self):
        return pd.read_csv(self.path, sep=';', parse_dates=['time'], date_format=datetime_format)

    def update_db(self, user: str, word_pl: str, lang: str, translation, was_correct: bool):
        df = pd.read_csv(self.path, sep=';')

        df = self.add_new_record(df, lang, translation, user, was_correct, word_pl)

        df.to_csv(self.path, index=False, sep=';')

    @staticmethod
    def add_new_record(df, lang, translation, user, was_correct, word_pl):
        new_row = pd.DataFrame({'user': user,
                                'word_pl': word_pl,
                                'lang': lang,
                                'translation': translation,
                                'correct': was_correct,
                                'time': dt.now().replace(microsecond=0)
                                }, index=[0])

        return pd.concat([df, new_row])

    # for now won't be used
    @staticmethod
    def update_record(df, past_record, was_correct):
        row_id = past_record.index[0]  # assumes that there's only one such record but there's no validation

        column_to_update = 'correct' if was_correct else 'wrong'

        df.loc[row_id, column_to_update] = past_record.loc[row_id, column_to_update] + 1
        df.loc[row_id, 'time'] = dt.now().replace(microsecond=0)

        return df
