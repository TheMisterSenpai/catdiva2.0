import discord
from discord.ext import commands
from discord.utils import get

from module.cybernetic.paginator import Paginator as pr

class setting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["настройки", True]

    @commands.command(
    	aliases=['настройки', 'setting'],
    )
    async def _setting(ctx, self):
    	embed1 = discord.Embed(title = 'test',
    		description = 'test1')
    	embed2 = discord.Embed(title = 'test2',
    		description = 'test2')

    	embeds = [embed1, embed2]
    	message = await ctx.send(embed = embed1)
    	page = pr(client, message, only = ctx.author, use_more = False, embeds = embeds)
    	await page.start()

def setup(client):
    client.add_cog(setting(client))     