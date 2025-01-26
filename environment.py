import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from actions.translation import TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH
from common.lib.utils import DEFAULT_USER_NAME
from vocabulary.lib.file_db import TranslationExerciseCSVHandler

load_dotenv()

def set_or_raise_error(var_name):
    environment_var = os.getenv(var_name)
    if environment_var is None:
        raise RuntimeError(f'{var_name} environment variable is not set')
    else:
        return environment_var


DATABASE = set_or_raise_error('DATABASE_URL')
DEEPL_API_KEY = set_or_raise_error('DEEPL_API_KEY')

engine = create_engine(DATABASE)

LOG_CSV_HANDLER = TranslationExerciseCSVHandler(TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH, DEFAULT_USER_NAME)
