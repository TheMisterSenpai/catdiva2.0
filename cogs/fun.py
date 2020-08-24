import discord
from discord.ext import commands
from discord.utils import get
import wikipedia
from random import randint, choice
import asyncio
import nekos
import datetime
import random 
from datetime import timedelta


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wiki(self, ctx, *, text):
        wikipedia.set_lang("ru")
        new_page = wikipedia.page(text)
        summ = wikipedia.summary(text)
        emb = discord.Embed(
            title= new_page.title,
            description= summ,
            color = 0x00ffff
         )
        emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

        await ctx.send(embed=emb)

    @commands.command(aliases = ['хент', 'hentai'])
    async def хентай(self, ctx):
        if ctx.channel.is_nsfw():
            r = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
            'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
            'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
            'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
            'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
            'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
            'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
            'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
            'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof'
		    ]
            rnek = nekos.img(random.choice(r))
            emb = discord.Embed(color = discord.Color.red())
            emb.set_image(url = rnek)
            await ctx.send(embed = emb)
        else:
            msg = await ctx.send(embed = discord.Embed(description='Не думаю, что это подходящий канал для такого контента...', color=discord.Color.orange()))
            await ctx.message.add_reaction('🔞')
            await asyncio.sleep(5)
            await msg.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен fun.py')       

def setup(client):
    client.add_cog(fun(client))     