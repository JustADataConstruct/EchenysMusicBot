import discord
from discord.ext import commands, tasks

import json
import sys
import os

class ValerieBot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.songs = self.load_songs()
        print(self.songs)
        self.songqueue = []
        self.nowplay = ""
        self.update_status.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected")

    @tasks.loop(minutes=1)
    async def update_status(self):
        print(f"NOWPLAY: {self.nowplay}")
        if self.nowplay == "":
            return
        elif self.nowplay == "STOP":
            await self.bot.change_presence(activity=None)
            self.nowplay = ""
            return
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=self.nowplay))                


    def load_songs(self):
        try:
            with open('songs.json') as f: #TODO: Would a database work better? Probably yes.
                s = f.read()
                sng = json.loads(s)
                return sng
        except Exception as e:
            print(e)

    @commands.command(name="alive", description="Check if I am working correctly.")
    async def ping(self,ctx):
        await ctx.send("I live, father.")

    @commands.command(name="join")
    async def join(self,ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Connected to {channel.name}")
        else:
            await ctx.send("You aren't in a voice channel.")

    @commands.command(name="leave")
    async def leave(self,ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I am not in voice channel.")

    @commands.command(name="play")
    async def play(self,ctx,name:str):
        try:
            if ctx.voice_client:
                song = self.songs[name.lower()]
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
                self.nowplay = os.path.basename(route)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=self.nowplay))                 
                await ctx.send(f"Playing {self.nowplay}")
        except Exception as e:
            await ctx.send("Song not found.")
            print(e)

    @commands.command(name="playlist")
    async def playlist(self,ctx,name:str):
        try:
            if type(self.songs[name.lower()]) == dict :
                await ctx.send("This is a single song, not a playlist. Use the 'play' command.")
                return
            length = len(self.songs[name.lower()])
            for song_object in self.songs[name.lower()]:
                self.songqueue.append(song_object)
            if not ctx.voice_client.is_playing():
                options = ""
                song = self.songqueue[0]
                route = song["route"]
                if 'start_point' in song:
                    sp = song["start_point"]
                    options += f"-ss {sp}"
                if 'end_point' in song:
                    ep = song["end_point"]
                    options += f" -to {ep}"
                await ctx.send(f"Playing playlist {name}, {length} songs.")            
                ctx.voice_client.play(discord.FFmpegPCMAudio(route,options=options),after=lambda e:self.play_next(ctx))
                self.nowplay = os.path.basename(route)
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=self.nowplay)) 
                print(f"Playing {route}")            
        except Exception as e:
            print(e)

    def play_next(self,ctx):
        if len(self.songqueue) == 0: return    
        del self.songqueue[0]
        if len(self.songqueue) >= 1:
            options = ""
            song = self.songqueue[0]
            route = song["route"]
            if 'start_point' in song:
                sp = song["start_point"]
                options += f"-ss {sp}"
            if 'end_point' in song:
                ep = song["end_point"]
                options += f" -to {ep}"            
            ctx.voice_client.play(discord.FFmpegPCMAudio(route,options=options),after=lambda e:self.play_next(ctx))
            self.nowplay = os.path.basename(route)            
            print(f"Playing {route}")        
        else:
            print("end of playlist.")
            self.nowplay = "STOP"

    @commands.command()
    async def stop(self,ctx):
        try:
            self.songqueue.clear()
            await self.bot.change_presence(activity=None)
            ctx.voice_client.stop()
        except:
            await ctx.send("Not playing anything.")

    @commands.command()
    async def pause(self,ctx):
        try:
            ctx.voice_client.pause()
        except:
            await ctx.send("Not playing anything.")

    @commands.command()
    async def resume(self,ctx):
        try:
            ctx.voice_client.resume()
        except:
            await ctx.send("Can't resume")

    @commands.command()
    async def skip(self,ctx):
        try:
            route = self.songqueue[1]["route"]
            self.nowplay = os.path.basename(route)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=self.nowplay))            
            ctx.voice_client.stop()
        except Exception as e:
            print(e)

    @commands.command()
    async def reload(self,ctx):
        self.songs = self.load_songs()
        print(self.songs)
        await ctx.send("Reloading song list.")

    @commands.command()
    async def disconnect(self,ctx):
        await ctx.send("Bye!")
        await bot.logout()
        print("Bot offline.")


intents = discord.Intents.default()
description = "Music bot for the Echenys server"

bot = commands.Bot('valerie ',description=description,intents=intents)
bot.add_cog(ValerieBot(bot))

token = ""
try:
    with open('token.txt') as f:
        token = f.read()
except:
    print("Can't find token file!")

bot.run(token)