import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

def get_db():
  CONNECTION_STRING = f'mongodb+srv://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PW")}@cluster0.wnxer5b.mongodb.net/?retryWrites=true&w=majority'
  client = MongoClient(CONNECTION_STRING)
  return client['msgDatabase']