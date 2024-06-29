from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME_SETUP = os.getenv('DB_NAME_SETUP')
DB_NAME_USE = os.getenv('DB_NAME_USE')

OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')