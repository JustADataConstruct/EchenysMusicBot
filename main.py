import discord
from discord.ext import commands

intents = discord.Intents.default()
description = "Music bot for the GCCM server"

bot = commands.Bot('/',description=description,intents=intents)

token = ""
try:
    with open('token.txt') as f:
        token = f.read()
except:
    print("Can't find token file!");

@bot.event
async def on_ready():
    print("Connected")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await message.channel.send("I hear you.")

bot.run(token)