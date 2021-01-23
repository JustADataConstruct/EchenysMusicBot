import discord
from discord.ext import commands

import json

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

def load_songs():
    try:
        with open('songs.json') as f: #TODO: Would a database work better? Probably yes.
            s = f.read()
            sng = json.loads(s)
            return sng
    except Exception as e:
        print(e)

songs = load_songs()
print(songs)
songqueue = []

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
async def play(ctx,name:str): #TODO: Check if playlist.
    try:
        if ctx.voice_client:
            song = songs[name.lower()]
            if type(song) == list :
                await ctx.send("This is a playlist, not a single song. Use the 'playlist' command.")
                return            
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            options= ""
            route = song["route"]
            if 'start_point' in song:
                sp = song["start_point"]
                options += f"-ss {sp}"
            if 'end_point' in song:
                ep = song["end_point"]
                options += f" -to {ep}"
            ctx.voice_client.play(discord.FFmpegPCMAudio(route,options=options),after=lambda e:print('done',e))
            print(f"Playing {route}")
            await ctx.send(f"Playing {name}")
    except Exception as e:
        await ctx.send("Song not found.")
        print(e)

@bot.command(name="playlist")
async def playlist(ctx,name:str):
    try:
        if type(songs[name.lower()]) == dict :
            await ctx.send("This is a single song, not a playlist. Use the 'play' command.")
            return
        for song_object in songs[name.lower()]:
            songqueue.append(song_object)
        if not ctx.voice_client.is_playing():
            options = ""
            song = songqueue[0]
            route = song["route"]
            if 'start_point' in song:
                sp = song["start_point"]
                options += f"-ss {sp}"
            if 'end_point' in song:
                ep = song["end_point"]
                options += f" -to {ep}"            
            ctx.voice_client.play(discord.FFmpegPCMAudio(route,options=options),after=lambda e:play_next(ctx))
            print(f"Playing {route}")            
    except Exception as e:
        print(e)

def play_next(ctx):
    if len(songqueue) == 0: return    
    del songqueue[0]
    if len(songqueue) >= 1:
        options = ""
        song = songqueue[0]
        route = song["route"]
        if 'start_point' in song:
            sp = song["start_point"]
            options += f"-ss {sp}"
        if 'end_point' in song:
            ep = song["end_point"]
            options += f" -to {ep}"            
        ctx.voice_client.play(discord.FFmpegPCMAudio(route,options=options),after=lambda e:play_next(ctx))
        print(f"Playing {route}")        
    else:
        print("end of playlist.")

@bot.command()
async def stop(ctx):
    try:
        songqueue.clear()
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

@bot.command()
async def skip(ctx):
    try:
        ctx.voice_client.stop()
    except Exception as e:
        print(e)

@bot.command()
async def reload(ctx):
    global songs
    songs = load_songs()
    print(songs)
    await ctx.send("Reloading song list.")

bot.run(token)