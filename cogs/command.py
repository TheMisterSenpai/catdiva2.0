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
        
        color = config.COLOR_GOOD

        prefix = collection.find_one({"guild_id": ctx.guild.id})["prefix"]

        copy_text = config.COPYRIGHT_TEXT
        copy_icon = config.COPYRIGHT_ICON

        cogs = []
        for i in self.client.cogs:
            cog = self.client.cogs[i]
            hide = len(cog.cog_name)
            if hide == 1:
                cogs.append(f"{cog.cog_name[0]}")
        '''
        if not name:
            embed = discord.Embed(
                description=f"{ctx.author.display_name}, Чтоб узнать список команд пропишите {prefix}хелп <модуль>\n"
                            f"**Доступные модули:** {', '.join(cogs)}")
            await ctx.send(embed=embed)
        '''    
    
        if name in cogs:
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
            

            embed = discord.Embed(
                title=f"Хелп | {name}",
                description=f"".join(comm_list),
                color=color)
            embed.set_footer(text=copy_text, icon_url=copy_icon)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/695787093242282055/707320024473534485/what.png')

            await ctx.send(embed=embed)
        
        else:
            embed = discord.Embed(
                description=f"{ctx.author.display_name}, Модуль не найден!\nЧтоб узнать список команд пропишите {prefix}команды\n")
            await ctx.send(embed=embed)
        
    
    @commands.command(
        aliases=["команды"],
        description="Это сообщение",
        usage="команды")
    async def _help(self, ctx, name=None):
        prefix = collection.find_one({"guild_id": ctx.guild.id})["prefix"]

        copy_text = config.COPYRIGHT_TEXT
        copy_icon = config.COPYRIGHT_ICON

        emb = discord.Embed(color= COLOR_GOOD, title=f'Вот все мои команды {ctx.author}!', description=f'''
❄Чтобы увидеть использования команд просто пропиши {prefix}хелп [модуль]❄

**администрация**
{prefix}бан, {prefix}разбан, {prefix}кик, 
{prefix}очистить, {prefix}голосование, {prefix}жалоба,
{prefix}мут

**интересные**
{prefix}вики, {prefix}хент, {prefix}юзеринфо, 
{prefix}личныесообщения, {prefix}номеринфо, {prefix}ачивка

**игры**
{prefix}монетка, {prefix}кнб, {prefix}сапер, {prefix}флаги

**информация**
{prefix}yt, {prefix}войстайм, {prefix}майн, {prefix}инфо

**любовь**
{prefix}обнять, {prefix}поцеловать

**музыка**
{prefix}играть, {prefix}очередь, {prefix}пауза, 
{prefix}громкость, {prefix}музыка?, {prefix}присоед,
{prefix}перезапустить, {prefix}пропустить, {prefix}выйти,
{prefix}повторить, {prefix}остановить, {prefix}пропустить

**Специальные**
{prefix}bag, {prefix}ping, {prefix}настройки,
{prefix}path

''')
        emb.set_footer(text=copy_text, icon_url=copy_icon)
        emb.set_thumbnail(url = self.client.user.avatar_url)
        await ctx.send(embed = emb)        
       

def setup(client):
    client.add_cog(command(client)) 