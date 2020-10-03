import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import requests
import re
import urllib.request
from urllib.parse import quote
import json
import os

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Информация"]

    @commands.command(
        aliases = ['инфо', 'info'],
        description='узнать о боте',
        usage='info'
    )
    async def _info(self, ctx):
        await ctx.send('**Привет, меня зовут Кошка Дива и я офицальный бот сервера "Убежище клоунов"**')
        await asyncio.sleep(5)
        await ctx.send('**Чтоб посмотреть все мои команды, просто напиши .help**')
        await asyncio.sleep(3)
        await ctx.send('**Если вы нашли баг или недоработку то напишите .bag или пишите моему разработчику** @TheMisterSenpai#2033')
        await asyncio.sleep(5)
        await ctx.send('**Мой исходный код: https://github.com/TheMisterSenpai/catdiva2.0 **')

    @commands.command(
        aliases=['сервер', 'серверинфо', 'server'],
        description="Информация о сервере",
        usage='server'
    )
    async def _server(self, ctx):
 
        members = ctx.guild.members
        bots = len([m for m in members if m.bot])
        users = len(members) - bots
        online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
        offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
        idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
        dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
        allvoice = len(ctx.guild.voice_channels)
        alltext = len(ctx.guild.text_channels)
        allroles = len(ctx.guild.roles)
 
        embed = discord.Embed(title=f"{ctx.guild.name}", color= 302112 , timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.guild.icon_url)
 
        embed.add_field(name=f"Пользователей", value=f"Участников: **{users}**\n"
                                                f"Ботов: **{bots}**\n"
                                                f"Онлайн: **{online}**\n"
                                                f"Отошёл: **{idle}**\n"
                                                f"Не Беспокоить: **{dnd}**\n"
                                                f"Оффлайн: **{offline}**")
 
        embed.add_field(name=f"Каналов", value=f"Голосовые: **{allvoice}**\n"
                                            f"Текстовые: **{alltext}**\n")
 
        embed.add_field(name=f"Уровень Буста", value=f"{ctx.guild.premium_tier} (Бустеров: {ctx.guild.premium_subscription_count})")
        embed.add_field(name=f"Количество Ролей", value=f"{allroles}")
        embed.add_field(name=f"Создатель сервера", value=f"{ctx.guild.owner}")
        embed.add_field(name=f"Регион сервера", value=f"{ctx.guild.region}")
        embed.add_field(name=f"Дата создания сервера", value=f"{ctx.guild.created_at.strftime('%b %#d %Y')}")
 
        embed.set_footer(text='Вызвал команду: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
  

    @commands.command(
        aliases=["yt"],
        description="Поиск на Ютуб.",
        usage="yt <Название>")
    async def youtube(self, ctx, *, title):
        video_id = []
        sq = f'https://www.youtube.com/results?search_query={quote(title)}&sp=EgIQAQ%253D%253D'  # quote приабразуем удобочитаемасть для адресной строки
        data = urllib.parse.urlencode({'Host': 'search.cpsa.ca', 'Connection': 'keep-alive', 'Content-Length': 23796,
                                       'Origin': 'http://search.cpsa.ca',
                                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                       'Cahce-Control': 'no-cache', 'X-Requested-With': 'XMLHttpRequest',
                                       'X-MicrosoftAjax': 'Delta=true', 'Accept': '*/*',
                                       'Referer': 'http://search.cpsa.ca/PhysicianSearch',
                                       'Accept-Encoding': 'gzip, deflate',
                                       'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
                                       'Cookie': 'ASP.NET_SessionId=kcwsgio3dchqjmyjtwue402c; _ga=GA1.2.412607756.1459536682; _gat=1'})
        data = data.encode('ascii')
        doc = urllib.request.urlopen(sq, data).read().decode('cp1251', errors='ignore')
        match = re.findall(r"\?v\=(.+?)\"", doc)  # Ищем на стронички все эти символы
        if not (match is None):  # Если мы нашли
            for ii in match:
                if (len(ii) < 25):  # 25 потомучто в строке поиска ютуба максимму 25 символов
                    video_id.append(ii)

        video_id = dict(zip(video_id, video_id)).values()  # Очищаем од дублей

        video_id = list(video_id)
        await ctx.send(f'https://www.youtube.com/watch?v={video_id[0]}')

def setup(client):
    client.add_cog(info(client)) 