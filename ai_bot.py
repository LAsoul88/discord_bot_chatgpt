# Note up top to make sure this is working

import os

import openai
import discord
from dotenv import load_dotenv

from user_map import user_map

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model_id = 'gpt-3.5-turbo'

def converse(conversation):
  messages = []
  messages.append({ "role": "user", "content": conversation })
  response = openai.ChatCompletion.create(
      model=model_id,
      messages=messages
  )
  return response

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  username = message.author.name
  query = f'{username} asks: {message.content}'
  
  if message.content.startswith('/help'):
    await message.channel.send('I would be happy to help! The following list of commands are available to you at this time:\n- /help - brings up list of available commands\n- /info [request] - asks chatgpt a question and returns information\n- /joke [subject] - returns a joke on the listed subject')

  # if message.content.startswith('/chat'):
  #    await message.channel.send("Let's have a chat!")
    
  # if message.content.startswith('/arbitration'):
  #     await message.channel.send("Let's settle a dispute!")

  if message.content.startswith('/info'):
    formatted_query = query.replace('/info ', '')
    print(f'query: {formatted_query}')
    reply = converse(formatted_query)["choices"][0]["message"]["content"]
    if len(reply) > 2000:
        print('reply > 2000')
        reply_list = [sentence + '.' for sentence in reply.split('.') if sentence]
        message_string = ''
        for idx, sentence in enumerate(reply_list):
            if len(sentence) + len(message_string) > 2000:
                print('sending message_string')
                await message.channel.send(message_string)
                message_string = sentence
            else:
                print('adding to message_string')
                message_string = message_string + sentence
                if idx == len(reply_list) - 1:
                   await message.channel.send(message_string)
    else:
        print(f'reply < 2000')
        await message.channel.send(reply)

  if message.content.startswith('/joke'):
    formatted_query = query.replace('/joke ', 'Can you tell me a joke about ')
    print(f'query: {formatted_query}')
    reply = converse(formatted_query)["choices"][0]["message"]["content"]
    print(f'reply: {reply}')
    await message.channel.send(reply)

client.run(TOKEN)
