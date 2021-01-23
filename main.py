import discord
from discord.ext import commands

intents = discord.Intents.default()
description = "Music bot for the Echenys server"

bot = commands.Bot('valerie ',description=description,intents=intents)

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

@bot.command(name="play")
async def play(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio('test.mp3'),after=lambda e:print('done',e))

@bot.command()
async def stop(ctx):
    try:
        ctx.voice_client.stop()
    except:
        await ctx.send("Not playing anything.")

@bot.command()
async def pause(ctx):
    try:
        ctx.voice_client.pause()
    except:
        await ctx.send("Not playing anything.")

@bot.command()
async def resume(ctx):
    try:
        ctx.voice_client.resume()
    except:
        await ctx.send("Can't resume")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "hello":
        await message.channel.send("Hi!")
        return
    await bot.process_commands(message)


bot.run(token)