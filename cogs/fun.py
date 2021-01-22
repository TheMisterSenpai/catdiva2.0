import discord
from discord.ext import commands
from discord.utils import get

import wikipedia
from random import randint, choice
import asyncio
import catdiva
import datetime
import random 
from datetime import timedelta

from module.catdivamodule import config

COPYRIGHT_TEXT = config.COPYRIGHT_TEXT
ICON = config.COPYRIGHT_ICON

заставка1 = 'https://media1.tenor.com/images/cc69621982e3b2af8d6840c0ded9b81a/tenor.gif?itemid=14496292'
заставка2 = 'https://avatars.mds.yandex.net/get-zen_doc/1110951/pub_5d48f6b6fc69ab00ac290316_5d4905f9bf50d500ae427c3f/orig'
заставка3 = 'https://i.gifer.com/LHkW.gif'
заставка4 = 'https://i.gifer.com/N8oR.gif'
заставка5 = 'https://i.gifer.com/XiPu.gif'
заставка6 = 'https://media.tenor.com/images/98637699e8810ed22c9879be997affe9/tenor.gif'
заставка7 = 'https://media.tenor.com/images/65d17e29caf114577bd9f3abce398e0d/tenor.gif'


class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name= ["интересные"]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[]интересные был запущин[]')
        
    @commands.command(
        aliases=['вики', 'wiki'],
        description='узнать информацию на вики',
        usage='wiki <информация>'
    )
    async def _wiki(self, ctx, *, text):
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

    @_wiki.error
    async def _wiki_error(self, ctx, error):
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            await ctx.message.delete()
            emb = discord.Embed()
            emb.add_field( name = ':x: Вики:', value = 'Использование команды: **вики** <текст>' )
            await ctx.send( embed = emb )    

    @commands.command(
        aliases = ['хент', 'hentai'],
        description='интересные gif',
        usage='hentai'
    )
    async def _хентай(self, ctx):
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
            rnek = catdiva.img(random.choice(r))
            emb = discord.Embed(color = discord.Color.red())
            emb.set_image(url = rnek)
            await ctx.send(embed = emb)
        else:
            await ctx.send(f'**Нигодяй**:\nПоявилась ошибка в команде: ``хент``\nПричина ошибки: **Не подходящий для этого контента канал**')
            emb.set_footer(text=COPYRIGHT_TEXT, icon_url=ICON)
            emb = discord.Embed(colour=discord.Color.orange())
            await ctx.message.add_reaction('🔞')
            await ctx.send(embed=emb)
            
    @commands.command(
        aliases=['юзеринфо', 'юзер', 'userinfo'],
        description='узнать о человеке на сервере',
        usage='userinfo <@ник>'
    )
    async def _userinfo(self, ctx, member: discord.Member):
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

    @commands.command( 
        aliases=['приветствие', 'send_l'],
        description='отправить приветствия пользователю',
        usage='send_l <@ник>'
    )
    async def _send_l( self, ctx, member: discord.Member ):
	    await member.send(f'✉️{ctx.author.name} приветствует тебя {member.mention}✉️')#приветствие 
	    await ctx.channel.purge( limit = 1)

    @commands.command(
        aliases=['номер', 'номеринфо', 'phone_info'],
        description='получить информацию о номере',
        usage='phone_info <+7 номер>'
    )
    async def _phone_info( self, ctx, arg ):
	    response = requests.get( f'https://htmlweb.ru/geo/api.php?json&telcod={ arg }' )

	    user_country = response.json()[ 'country' ][ 'english' ]
	    user_id = response.json()[ 'country' ][ 'id' ]
	    user_location = response.json()[ 'country' ][ 'location' ]
	    user_city = response.json()[ 'capital' ][ 'english' ]
	    user_width = response.json()[ 'capital' ][ 'latitude' ]
	    user_lenth = response.json()[ 'capital' ][ 'longitude' ]
	    user_post = response.json()[ 'capital' ][ 'post' ]
	    user_oper = response.json()[ '0' ][ 'oper' ]

	    global all_info
	    all_info = f'<INFO>\nCountry : { user_country }\nID : { user_id }\nLocation : { user_location }\nCity : { user_city }\nLatitude : { user_width }\nLongitude : { user_lenth }\nIndex post : { user_post }\nOperator : { user_oper }'

	    await ctx.author.send( all_info )
	    await ctx.channel.purge( limit = 1)

          
    @commands.command(
        aliases=['achivment', 'ачивка'],
        description ='создать свои ачивку из майнкрафта',
        usage='ачивка <текст> (на английском языке)'
    )
    async def ach(self, ctx, *, text=None):
        if text is None:
            embed = discord.Embed(title='Ошибка', description=f'Укажите текст `ach <текст на англ.языке>`', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            a = random.randint(1, 40)
            done = text.replace(' ', '+')
            link = f'https://minecraftskinstealer.com/achievement/{a}/Achievement+Get%21/{done}'
            embed = discord.Embed(title='Получено Достижение!', color=discord.Color.green())
            embed.set_image(url=link)
            await ctx.send(embed=embed)

    @commands.command(
        aliases = ['заставка'],
        description = 'случайно выбирает заставку из разных мемов',
        usage = 'заставка'
    )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def screensaver(self, ctx):

        emb = discord.Embed(title = f'**Заставка**', color=0xffc0cb)
        emb.set_image(url = random.choice([заставка1, заставка2, заставка3, заставка4, заставка5, заставка6, заставка7])) 
        emb.set_footer(text=f'Вызвано: {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
        await ctx.send(embed=emb)
            
def setup(client):
    client.add_cog(fun(client))     