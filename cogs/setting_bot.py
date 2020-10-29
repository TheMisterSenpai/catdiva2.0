import discord
from discord.ext import commands
from discord.utils import get

import os

class setting_bot(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Настройки"]

    @commands.command(
        aliases = ['загрузитьког', 'load'],
        description = 'загрузить ког из папки cogs',
        usage = 'load <ког>'
    )
    async def _load(self, ctx, extensions):
        if ctx.author.id == 364437278728388611:
            client.load_extension(f'cogs.{extensions}')
        else:
            await ctx.send(f'Вы не создатель {ctx.author}')

    @commands.command(
        aliases = ['перезагрузитьког', 'reload'],
        description = 'перезагрузить ког из папки cogs',
        usage = 'reload <ког>'
    )
    async def _reload(self, ctx, extensions):
        if ctx.author.id == 364437278728388611:
            client.unload_extension(f'cogs.{extensions}')
            client.load_extension(f'cogs.{extensions}')
        else:
            await ctx.send(f'Вы не создатель {ctx.author}')

    @commands.command(
        aliases = ['выгрузитьког', 'unload'],
        description = 'выгрузить ког из папки cogs',
        usage = 'unload <ког>'
    )
    async def _unload(self, ctx, extensions):
        if ctx.author.id == 364437278728388611:
            client.unload_extension(f'cogs.{extensions}')
        else:
            await ctx.send(f'Вы не создатель {ctx.author}')

    @commands.command(
        aliases=['голосование', 'quickpoll'],
        description = 'устроить голосование',
        usage = 'голосование <текст>'
    )
    @commands.has_permissions( administrator = True) 
    async def poll(self, ctx, *, question=None):
        if question is None:
            embed = discord.Embed(title="Ошибка", description="Укажите тему голосования!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Голосование", description=f"{question}\n👍 - Да\n👎 - Нет", color=discord.Color.green())
            bruh = await ctx.send(embed=embed)
            await bruh.add_reaction("👍")
            await bruh.add_reaction("👎") 

    @commands.command(
        aliases=['смотреть', 'view'],
        description = 'посмотреть содержимое бота :D',
        usage = 'смотреть'
    )
    async def _view(self, ctx):
        directory = os.getcwd()
        list_files = os.listdir(directory)
        files_and_folders = "\n".join(list_files)
        await ctx.send(files_and_folders)               

def setup(client):
    client.add_cog(setting_bot(client))        