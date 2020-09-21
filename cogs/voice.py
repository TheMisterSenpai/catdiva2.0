import discord
from discord.ext import commands
import json
import asyncio
 
class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
        self.cog_name = ["Голосовое"]
 
    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            with open("./Data/DataBase/voices.json", "r") as file:
                data = json.load(file)
 
            for guild in self.bot.guilds:
                if str(guild.id) not in data.keys():
                    data[str(guild.id)] = {}
 
                voices = [channel for channel in guild.voice_channels]
                members = [channel.members for channel in voices]
                ids = []
                for lst in members:
                    for member in lst:
                        ids.append(member.id)
 
                if len(ids) <= 0:
                    continue
 
                for member in ids:
                    if str(member) not in data[str(guild.id)].keys():
                        data[str(guild.id)][str(member)] = 0
 
                    elif member in self.prev:
                        data[str(guild.id)][str(member)] += 1
                    
                    else:
                        self.prev.append(member)
 
            with open("./Data/DataBase/voices.json", "w") as file:
                json.dump(data, file, indent = 4)
 
            await asyncio.sleep(1)
 
    @commands.command(
        aliases=['войстайм', 'voicetime'],
        description='сколько вы были в голосовых чата',
        usage='voicetime'
    )
    async def _voicetime(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
 
        with open("./Data/DataBase/voices.json", "r") as file:
            data = json.load(file)
 
        if str(ctx.guild.id) not in data.keys():
            data[str(ctx.guild.id)] = {}
        
        if str(member.id) not in data[str(ctx.guild.id)].keys():
            data[str(ctx.guild.id)][str(member.id)] = 0
        
        seconds = data[str(ctx.guild.id)][str(member.id)]
        seconds = seconds % (24 * 3600)
        days = seconds // (60 * 60 * 24)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
 
        await ctx.send(embed = discord.Embed(title = "Voice time", description = f"In Voice: {days} day(s) {hours} hour(s) {minutes} minute(s) {seconds} second(s)", color = 190090))
 
def setup(bot):
    bot.add_cog(voice(bot))