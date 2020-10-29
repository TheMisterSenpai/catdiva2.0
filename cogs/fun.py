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
        self.cog_name= ["интересные"]    
        
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
            rnek = nekos.img(random.choice(r))
            emb = discord.Embed(color = discord.Color.red())
            emb.set_image(url = rnek)
            await ctx.send(embed = emb)
        else:
            msg = await ctx.send(embed = discord.Embed(description='Не думаю, что это подходящий канал для такого контента...', color=discord.Color.orange()))
            await ctx.message.add_reaction('🔞')
            await asyncio.sleep(5)
            await msg.delete()

    @commands.command(
        aliases=['юзеринфо', 'юзер', 'userinfo'],
        description='узнать о человеке',
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
        aliases=['личныесообщения', 'лс', 'send_l'],
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
            embed = discord.Embed(title='Ошибка', description=f'Укажите текст `>ach <text>`', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            a = random.randint(1, 40)
            done = text.replace(' ', '+')
            link = f'https://minecraftskinstealer.com/achievement/{a}/Achievement+Get%21/{done}'
            embed = discord.Embed(title='Получено Достижение!', color=discord.Color.green())
            embed.set_image(url=link)
            await ctx.send(embed=embed)
        
def setup(client):
    client.add_cog(fun(client))     