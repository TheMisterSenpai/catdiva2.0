import discord
from discord.ext import commands
from discord.utils import get

import json
import asyncio

class event(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.prev = []
        self.cog_name = ["Ивенты", True]
    #Зачем ты зашел в этот файл, он так для красоты

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

    @commands.Cog.listener()
    async def on_message(self, message):
        splited = message.content.split(' ')
        if message.author.bot is False:
            if f'<@!737324393117778020>' in splited[0]:
                try:
                    if splited[1] is None:
                        # это пртосто чек
                        pass
                    else:
                        pass
                except:
                    e = discord.Embed(color=default, title=f'Привет {message.author.display_name}!', description=f'''
👋 Привет! Меня зовут **Кошка Дива 2.0**!

😎 Мой префикс: '.'
🤣 Я была создана чтобы поднять тебе настроение!
😲 Напиши команду `.хелп` чтобы узнать все мои возможности!
🤔 Нужна помощь по боту, или нашел баг/ошибку? Заходи на наш [сервер поддержки] https://discord.gg/n93aGfa!

🍀 Удачи!
''')
                    e.set_thumbnail(url=self.client.user.avatar_url)
                    await message.channel.send(embed=e)
            else:
                pass
        else:
            pass        
              
def setup(client):
    client.add_cog(event(client))                