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
import socket
from mcstatus import MinecraftServer
from module.catdivamodule import config

COLOR_GOOD = config.COLOR_GOOD

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["информация"]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[]информация был загружен[]')

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
 
        await ctx.send(embed = discord.Embed(title = "Голосовое время", description = f"В голосовом чате: {days} дней {hours} часы {minutes} минуты {seconds} секунды", color = 190090))
        
    @commands.command(
        aliases=["майн", "мс", "minecraft", "mine"],
        usage="mc <ip> [port]",
        description="Информация о Minecraft сервере")
    async def _mc(self, ctx, ip, port=None):
        message = await ctx.send("Идёт сбор информации, пожалуйста подождите.")
 
        if port is None:
            server = MinecraftServer.lookup(f"{ip}:25565")
        else:
            try:
                server = MinecraftServer.lookup(f"{ip}:{port}")
            except ValueError:
                embed = discord.Embed(title="Ошибка Подключения", description="Порт вне допустимого диапазона **0-65535**.",
                                      color=0xb20000)
                await message.delete()
                return await ctx.send(embed=embed)
 
        try:
            server_ping = server.ping()
            server_status = server.status()
 
        except socket.timeout:
            players = "`❌ Не Доступно`"
            version = "`❌ Не Доступно`"
            description = "`❌ Не Доступно`"
            ping = "`❌ Не Доступно`"
            status = "🔴 Отключен"
 
        except socket.gaierror:
            embed = discord.Embed(title="Ошибка Ввода", description="Вы ввели не действительный IP или Порт.", color=0xb20000)
            await message.delete()
            return await ctx.send(embed=embed)
 
        except IOError as error:
            embed = discord.Embed(title="Ошибка Подключение", description="Мне не удалось получить информацию с этого сервера.\n"
                                                                          "Возможно у него стоит какая-та защита.\n\n"
                                                                          f"`Ошибка: {error}`",
                                  color=0xb20000)
            await message.delete()
            return await ctx.send(embed=embed)
 
        else:
            players = f"{server_status.players.online}/{server_status.players.max}"
            version = server_status.version.name
 
            if 'extra' in server_status.description:
                description = f"\n- {server_status.description['extra'][0]['text']}\n" \
                              f"- {server_status.description['extra'][1]['text']}\n" \
                              f"- {server_status.description['extra'][2]['text']}"
            else:
                description = server_status.description['text']
 
            ping = server_ping
            status = "🟢 Включен"
 
        if status == "🟢 Включен":
            try:
                server_query = server.query()
 
            except socket.timeout:
                query = "Query отключен на сервере"
 
            else:
                query = f"**Хост:** {server_query.host}\n" \
                        f"**Софт:** {server_query.software}\n" \
                        f"**MOTD:** {server_query.motd}\n" \
                        f"**Плагины:** {''.join(server_query.plugins)}\n" \
                        f"**Игроки:** {', '.join(server_query.players.names)}"
 
        else:
            query = "`❌ Не Доступно`"
 
        embed = discord.Embed(
            title="Статус Travedit Сервер",
            description=f"**IP:** {ip}\n"
                        f"**Описание:** {description}\n"
                        f"**Версия:** {version}",
            color=0xFF7F3F)
        embed.add_field(name="Игроки", value=players, inline=False)
        embed.add_field(name="Статус", value=status, inline=False)
        embed.add_field(name="Пинг", value=ping, inline=False)
        embed.add_field(name="Данные через Query",
                        value=query,
                        inline=False)
 
        await message.edit(content=None, embed=embed)            


    @commands.command(
        aliases = ['инфо', 'info'],
        description='узнать о боте',
        usage='info'
    )
    async def _info(self, ctx):
        emb = discord.Embed(color= COLOR_GOOD, title=f'Привет {ctx.author}!', description=f'''
👋 Привет! Меня зовут **Кошка Дива 2.0**!

😎 Мой префикс: 'd.'
🤣 Я была создана чтобы поднять тебе настроение!
😲 Напиши команду `d.хелп` чтобы узнать все мои возможности!
😽 Пригласи меня на свой сервер ``d.приглаш``
😉 Можно настроить сервер через меня, просто пропиши d.настройки(БЕТА-ТЕСТ)
🤔 Нужна помощь по боту, или нашел баг/ошибку? Заходи на наш [сервер поддержки] https://discord.gg/aZfHSjR
😺 Мой открытый исходный код: https://github.com/TheMisterSenpai/catdiva2.0

🍀 Удачи!
''')
        emb.set_thumbnail(url = self.client.user.avatar_url)
        await ctx.send(embed = emb)    

def setup(client):
    client.add_cog(info(client)) 