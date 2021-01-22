import discord
from discord.ext import commands

intents = discord.Intents.default()
description = "Music bot for the Echenys server"

bot = commands.Bot('!',description=description,intents=intents)

token = ""
try:
    with open('token.txt') as f:
        token = f.read()
except:
    print("Can't find token file!")

@bot.event
async def on_ready():
    print("Connected")


@bot.command(name="alive", description="Check if I am working correctly.")
async def ping(ctx):
    await ctx.send("I live, father.")

@bot.command(name="join")
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Connected to {channel.name}")
    else:
        await ctx.send("You aren't in a voice channel.")

@bot.command(name="leave")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not in voice channel.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "hello":
        await message.channel.send("Hi!")
        return
    await bot.process_commands(message)


bot.run(token)