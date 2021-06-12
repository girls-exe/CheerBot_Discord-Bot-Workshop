import os
import discord
import requests
import json
import random
from replit import db

my_secret = os.environ['TOKEN']

client = discord.Client()

bag_words = ["worried", "anxious", "sad", "depressed", "unhappy", "gloomy", "angry", "mad", "miserable"]

starter_cheers = [
  "Nobody is perfect, and that is ok.",
  "All you can do is try your best.",
  "I believe in you.",
  "Cheer up!"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']
  return quote

def update_db(new_phrase):
  if "cheers" in db.keys():
    cheers = db["cheers"]
    cheers.append(new_phrase)
    db["cheers"] = cheers
  else:
    db["cheers"] = [new_phrase]

def delete_phrase(index):
  cheers = db["cheers"]
  if len(cheers) > index:
    del cheers[index]
    db["cheers"] = cheers

@client.event
async def on_ready():
  print("Bot is ready")

@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return

  if msg.startswith('!greetings'):
    await message.channel.send('Hi there!')

  if msg.startswith('!inspire'):
    await message.channel.send(get_quote())

  cheers_phrases = starter_cheers
  if "cheers" in db.keys():
    cheers_phrases.extend(db["cheers"])

  if any(word in msg for word in bag_words):
    await message.channel.send(random.choice(cheers_phrases))
  
  if msg.startswith('!add'):
    phrase = msg.split("!add ", 1)[1]
    update_db(phrase)
    await message.channel.send("New cheers phrase added.")

  if msg.startswith('!del'):
    cheers = []
    if "cheers" in db.keys():
      index = int(msg.split("!del", 1)[1])
      delete_phrase(index)
      cheers = db["cheers"]
    await message.channel.send(cheers)
  
  if msg.startswith('!list'):
    cheers = []
    if "cheers" in db.keys():
      cheers = db["cheers"]
    await message.channel.send(cheers)

client.run(my_secret)