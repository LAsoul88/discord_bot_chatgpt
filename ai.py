import os
from datetime import datetime

import openai
from dotenv import load_dotenv

from db import get_db

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

db = get_db()

class Brain:
    
  def __init__(self, user):
    self.user = user
    self.model = 'gpt-3.5-turbo'
    self.message_chain = []

  def __str__(self):
    return f'{self.user}'

  # handles formatting of call to openai API and returns response
  def converse(self, content, directive):
    self.message_chain.append({ 'role': 'system', 'content': directive })
    self.message_chain.append({ 'role': 'user', 'content': content })
    response = openai.ChatCompletion.create(
      model=self.model,
      messages=self.message_chain
    )['choices'][0]['message']['content']
    return response