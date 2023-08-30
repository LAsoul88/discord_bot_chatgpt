import os
from datetime import datetime

import openai
from dotenv import load_dotenv

from db import get_db

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

db = get_db()