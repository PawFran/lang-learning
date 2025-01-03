import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from actions.translation import TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH
from common.lib.utils import DEFAULT_USER_NAME
from vocabulary.lib.file_db import TranslationExerciseCSVHandler

load_dotenv()

DATABASE = os.getenv('DATABASE_URL')
if DATABASE is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE)

LOG_CSV_HANDLER = TranslationExerciseCSVHandler(TRANSLATION_EXERCISE_CSV_LOG_FILE_PATH, DEFAULT_USER_NAME)
