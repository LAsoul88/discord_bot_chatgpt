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
    self.collection = db[user]

  def __str__(self):
    return f'{self.user}'
  
  # records a message and adds to db
  def record(self, message, role):
    self.collection.insert_one({ 'role': role, 'content': message, 'timestamp': datetime.now() })

  # handles formatting of call to openai API and returns response
  def converse(self, content, directive):
    self.record(content, 'user')
    message_history = self.collection.find().sort('timestamp', -1)
    self.message_chain.append({ 'role': 'system', 'content': directive })

    # for cost reasons, this loop breaks after 4 messages have been gathered
    # it can be changed or eliminated altogether depending on the server's needs/resources
    for idx, message in enumerate(message_history):
      if idx > 4:
        break
      self.message_chain.append({ 'role': message['role'], 'content': message['content'] })

    self.message_chain.append({ 'role': 'user', 'content': content })
    response = openai.ChatCompletion.create(
      model=self.model,
      messages=self.message_chain
    )['choices'][0]['message']['content']
    self.record(response, 'assistant')
    return response