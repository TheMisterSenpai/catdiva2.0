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

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, member: discord.Member):
        roles = member.roles
        role_list = ""
        for role in roles:
            role_list += f"<@&{role.id}> "
        emb = discord.Embed(title=f'Информация о пользователе {member}', colour = 0x179c87)
        emb.set_thumbnail(url=member.avatar_url)
        emb.add_field(name='ID', value=member.id)
        emb.add_field(name='Имя', value=member.name)
        emb.add_field(name='Высшая роль', value=member.top_role)
        emb.add_field(name='Дискриминатор', value=member.discriminator)
        emb.add_field(name='Присоеденился к серверу', value=member.joined_at.strftime('%Y.%m.%d \n %H:%M:%S'))
        emb.add_field(name='Присоеденился к Discord', value=member.created_at.strftime("%Y.%m.%d %H:%M:%S"))
        emb.add_field(name='Роли', value=role_list)
        emb.set_footer(text='Вызвал команду: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed = emb)

    @commands.command( pass_context = True)
    async def send_l( self, ctx, member: discord.Member ):
	    await member.send(f'✉️{ctx.author.name} приветствует тебя {member.mention}✉️')#приветствие 
	    await ctx.channel.purge( limit = 1)

    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен fun.py')       

def setup(client):
    client.add_cog(fun(client))     