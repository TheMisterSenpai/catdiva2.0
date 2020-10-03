import discord
from discord.ext import commands
from discord.utils import get

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

def setup(client):
    client.add_cog(setting_bot(client))        