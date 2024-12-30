import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from actions.translation import TRANSLATION_EXERCISE_CSV_LOG_FILE
from common.lib.utils import DEFAULT_USER_NAME
from vocabulary.lib.file_db import TranslationExerciseCSVHandler

# Explicitly load the .env file
# load_dotenv(dotenv_path='/path/to/your/project/.env')
load_dotenv()

DATABASE = os.getenv('DATABASE_URL')
if DATABASE is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE)

LOG_CSV_HANDLER = TranslationExerciseCSVHandler(TRANSLATION_EXERCISE_CSV_LOG_FILE, DEFAULT_USER_NAME)
