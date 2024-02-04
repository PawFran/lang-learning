import os
import pandas as pd
from sklearn.model_selection import train_test_split
from pycaret.classification import *

path = os.path.join('vocabulary', 'db', 'translation_exercise_results.csv')

raw_df = pd.read_csv(path, sep=';', parse_dates=['time'])

df = raw_df.query('user == "default_user"')\
           .query('lang == "latin"')\
           .drop(['user', 'lang','session_id', 'correct_translation', 'user_answer'], axis=1)\
           .replace(True, 1)\
           .replace(False, 0)\
           .sort_values(['word_pl', 'time'])

time_shift = df.groupby('word_pl')['time'].shift(1).to_frame().rename(columns={'time': 'time_shift'})

was_last_correct = df.groupby('word_pl')['is_correct'].shift(1).to_frame().rename(columns={'is_correct': 'was_last_correct'})

df_with_timeshift_tmp = df.join(time_shift).join(was_last_correct)

time_col = df_with_timeshift_tmp.time
timeshift_col = df_with_timeshift_tmp.time_shift
time_diff_col = (time_col - timeshift_col)

df_with_timeshift = df_with_timeshift_tmp\
                        .assign(when_last_asked = time_diff_col)\
                        .drop(['time', 'time_shift'], axis=1)\
                        .query('when_last_asked != "NaT"')

df_with_timeshift['when_last_asked_min'] = (df_with_timeshift.when_last_asked.values / 60).astype('timedelta64[s]').astype('int')

df_final = df_with_timeshift.drop('when_last_asked', axis=1)

train, test = train_test_split(df_final, test_size=0.25, random_state=42, shuffle=True)

s = setup(train, target='is_correct')
best = compare_models()
evaluate_model(best)
predictions = predict_model(best, data=test)

print(f'dummy classifier\' accuracy (always true): {df_final.is_correct.sum() / len(df_final)}')
