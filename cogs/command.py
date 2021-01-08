import discord
from discord.ext import commands
from discord.utils import get

from module.catdivamodule import config
from module.catdivamodule import api

from pymongo import MongoClient

MONGO = api.MONGO

cluster = MongoClient(MONGO)
collection = cluster.catdivadb.prefixsett

COLOR_GOOD = config.COLOR_GOOD

class command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
        self.cog_name = ["command", True]

    @commands.command(
        aliases=["хелп", "comms", "commands", "помощь"],
        description="Это сообщение",
        usage="хелп [модуль]")
    async def help(self, ctx, name=None):
        prefix = collection.find_one({"guild_id": ctx.guild.id})["prefix"]
        color = config.COLOR_GOOD

        copy_text = config.COPYRIGHT_TEXT
        copy_icon = config.COPYRIGHT_ICON

        cogs = []
        for i in self.client.cogs:
            cog = self.client.cogs[i]
            hide = len(cog.cog_name)
            if hide == 1:
                cogs.append(f"{cog.cog_name[0]}")

        if not name:
            emb = discord.Embed(color= COLOR_GOOD, title=f'Вот все мои команды {ctx.author}!', description=f'''
❄Чтобы увидеть использования команд просто пропиши {prefix}хелп [модуль] (Например: {prefix}хелп музыка)❄

**администрация**
{prefix}бан, {prefix}разбан, {prefix}кик, 
{prefix}очистить, {prefix}голосование, {prefix}жалоба,
{prefix}мут, {prefix}размут

**интересные**
{prefix}вики, {prefix}хент, {prefix}юзеринфо, 
{prefix}личныесообщения, {prefix}номеринфо, {prefix}ачивка,
{prefix}заставка

**игры**
{prefix}монетка, {prefix}кнб, {prefix}флаги

**информация**
{prefix}войстайм, {prefix}майн, {prefix}инфо

**любовь**
{prefix}обнять, {prefix}поцеловать, {prefix}тыкнуть

**музыка**
{prefix}играть, {prefix}очередь, {prefix}пауза, 
{prefix}громкость, {prefix}музыка?, {prefix}присоед,
{prefix}перезапустить, {prefix}пропустить, {prefix}выйти,
{prefix}повторить, {prefix}остановить, {prefix}пропустить

**Специальные**
{prefix}bag, {prefix}ping, {prefix}настройки,
{prefix}path, {prefix}приглаш

''')    
            emb.set_footer(text=copy_text, icon_url=copy_icon)
            emb.set_thumbnail(url = self.client.user.avatar_url)
            await ctx.send(embed = emb)              
    
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
                title=f"Хелп | {name}",
                description=f"".join(comm_list),
                color=color)
            emb.set_footer(text=copy_text, icon_url=copy_icon)
            emb.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/695787093242282055/707320024473534485/what.png')

            await ctx.send(embed=emb)

def setup(client):
    client.add_cog(command(client)) 