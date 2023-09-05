import os

import discord
from dotenv import load_dotenv

from ai import Brain

load_dotenv()

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
  brain = Brain(username)
  
  if message.content.startswith('/help'):
    await message.channel.send('I would be happy to help! The following list of commands are available to you at this time:\n- /help - brings up list of available commands\n- /info [request] - asks chatgpt a question and returns information\n- /chat [request] - have a convo and see where things go\n- /joke [subject] - returns a joke on the listed subject')

  if message.content.startswith('/chat'):
    formatted_query = query.replace('/chat ', '')
    reply = await brain.converse(formatted_query, f'Chat casually with {username} about the subject they bring up. Responses are expected to be light, fun, and silly!')
    for section in reply:
      await message.channel.send(section)

  if message.content.startswith('/info'):
    formatted_query = query.replace('/info ', '')
    reply = await brain.converse(formatted_query, f'Please help {username} with gathering information and address them as {username}. Please be descriptive, longer form answers are welcome.')
    for section in reply:
      await message.channel.send(section)

  if message.content.startswith('/joke'):
    formatted_query = query.replace('/joke ', 'Can you tell me a joke about ')
    reply = brain.converse(formatted_query, 'Please bring some wit and cleverness to the joke you provide.')
    await message.channel.send(reply)

client.run(TOKEN)