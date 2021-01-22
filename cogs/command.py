import discord
from discord.ext import commands
from discord.utils import get

from module.catdivamodule import config
from module.catdivamodule import api
from utils import color
from naomi_paginator import Paginator

from pymongo import MongoClient

MONGO = api.MONGO

cluster = MongoClient(MONGO)
collection = cluster.catdivadb.prefixsett

COLOR_GOOD = color.COLOR_GOOD

class command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
        self.cog_name = ["command", True]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[]command был запущин[]')

    @commands.command(
        aliases=["хелп", "comms", "commands", "помощь"],
        description="Это сообщение",
        usage="хелп [модуль]")
    async def help(self, ctx, name=None):
        prefix = collection.find_one({"guild_id": ctx.guild.id})["prefix"]

        copy_text = config.COPYRIGHT_TEXT
        copy_icon = config.COPYRIGHT_ICON

        cogs = []
        for i in self.client.cogs:
            cog = self.client.cogs[i]
            hide = len(cog.cog_name)
            if hide == 1:
                cogs.append(f"{cog.cog_name[0]}")

        if not name:
            p = Paginator(ctx)

            embeds = (discord.Embed(color=0xffc0cb, title='<**Все мои команды**🗳>:',
                                    description=f'Чтобы увидеть использования команд просто пропиши {prefix}хелп [модуль] (Например: {prefix}хелп музыка) '),
                      discord.Embed(color=0xffc0cb, title='<**администрация**🗳>:',
                                    description=f'{prefix}бан, {prefix}разбан, {prefix}кик,\n{prefix}очистить, {prefix}голосование, {prefix}жалоба,\n{prefix}мут, {prefix}размут\n<**Описание🔎**>:\n``Команды для администрации серверов``'),
                      discord.Embed(color=0xffc0cb, title='<**интересные**🗳>:',
                                    description=f'{prefix}вики, {prefix}хент, {prefix}юзеринфо,\n{prefix}личныесообщения, {prefix}номеринфо, {prefix}ачивка, {prefix}заставка\n<**Описание🔎**>:\n``Команды для веселья``'),
                      discord.Embed(color=0xffc0cb, title='<**игры**🗳>:',
                                    description=f'{prefix}монетка, {prefix}кнб, {prefix}флаги\n<**Описание🔎**>:\n``Мини-игры для участников сервера``'),
                      discord.Embed(color=0xffc0cb, title='<**информация**🗳>:',
                                    description=f'{prefix}войстайм, {prefix}майн, {prefix}инфо\n<**Описание🔎**>:\n``Команды для ввода любой информации``'),
                      discord.Embed(color=0xffc0cb, title='<**музыка**🗳>:',
                                    description=f'{prefix}играть, {prefix}очередь, {prefix}пауза,\n{prefix}громкость, {prefix}музыка?, {prefix}присоед,\n{prefix}перезапустить, {prefix}пропустить, {prefix}выйти,\n{prefix}повторить, {prefix}остановить, {prefix}пропустить\n<**Описание🔎**>:\n``Команды для прослушивания музыки с YouTube`` '),
                      discord.Embed(color=0xffc0cb, title='<**Специальные**🗳>:',
                                    description=f'{prefix}bag, {prefix}ping, {prefix}настройки,\n{prefix}path, {prefix}приглаш\n<**Описание🔎**>:\n``Специальные команды для бота(Их нельзя найти в боте, но они работают :D)``'))

            for x in embeds:
                p.add_page(x)

            await p.call_controller()
    
        elif name in cogs:
            cog = None
            namec = None
            for i in self.client.cogs:
                coge = self.client.cogs[i]
                if name in coge.cog_name:
                    cog = coge
                    namec = i
                    break

            name = cog.cog_name[0]
            comm_list = []

            for command in self.client.commands:
                if command.cog_name == namec:
                    if not command.hidden:
                        comm_list.append(
                            f"**{command.aliases[0]}:** {command.description}\n`{prefix}{command.usage}`\n\n")
            

            emb = discord.Embed(
                title=f"<**Хелп**📖>:``{name}``",
                description=f"".join(comm_list),
                color=0xffc0cb)
            emb.set_footer(text=copy_text, icon_url=copy_icon)

            await ctx.send(embed=emb)

def setup(client):
    client.add_cog(command(client)) 