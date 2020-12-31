import discord
from discord.ext import commands
from discord.utils import get

import random

# Картинки :D
kek = "https://lifeo.ru/wp-content/uploads/gikfi-obnimashki-782.gif"
lol = "https://cdn.humoraf.ru/wp-content/uploads/2017/07/gif-21-10.gif"
rfr = "https://i.pinimg.com/originals/ba/a8/0b/baa80b2c50561bd5d95fe0aec61a1251.gif"
tgt = "https://media4.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif"
yhy = "https://i.pinimg.com/originals/f2/80/5f/f2805f274471676c96aff2bc9fbedd70.gif"
uju = "https://media.tenor.com/images/b6d0903e0d54e05bb993f2eb78b39778/tenor.gif"
img5 = "https://thumbs.gfycat.com/AlienatedFearfulJanenschia-small.gif"
img6 = "https://media1.tenor.com/images/b0de026a12e20137a654b5e2e65e2aed/tenor.gif?itemid=7552093"
img7 = "https://i.imgur.com/r9aU2xv.gif"
img8 = "https://media0.giphy.com/media/VHwgHhJLuWt0gjjUzf/source.gif"
img9 = "https://media2.giphy.com/media/lrr9rHuoJOE0w/200.gif"
img10 = "https://64.media.tumblr.com/18fdf4adcb5ad89f5469a91e860f80ba/tumblr_oltayyHynP1sy5k7wo1_400.gifv"
img11 = "https://25.media.tumblr.com/tumblr_ma7l17EWnk1rq65rlo1_500.gif"
img12 = "https://data.whicdn.com/images/45718472/original.gif"
img13 = "https://25.media.tumblr.com/2a3ec53a742008eb61979af6b7148e8d/tumblr_mt1cllxlBr1s2tbc6o1_500.gif"
img14 = "https://media.tenor.com/images/ca88f916b116711c60bb23b8eb608694/tenor.gif"
img15 = "https://otakulounge.files.wordpress.com/2019/02/picture1.gif"
img16 = "https://i.gifer.com/AHb9.gif"
img17 = "https://media0.giphy.com/media/sUIZWMnfd4Mb6/giphy.gif"
img18 = "https://dailysmscollection.org/wp-content/uploads/2019/01/anime-hug-gif.gif"
чмок1 = 'https://media.tenor.com/images/b020758888323338c874c549cbca5681/tenor.gif'
чмок2 = 'https://media.tenor.com/images/0492d81e001f66de4ec215b5d602e422/tenor.gif'
чмок3 = 'https://media.tenor.com/images/8a35d0f0a27c40d8886740a8b8e15592/tenor.gif'
чмок4 = 'https://media.tenor.com/images/29b22bb26ecc0943c95b9a1be81d3054/tenor.gif'
чмок5 = 'https://media.tenor.com/images/fbb2b4d5c673ffcf8ec35e4652084c2a/tenor.gif'
чмок6 = 'https://media.tenor.com/images/02026b4b33db655035803421fdf7d41c/tenor.gif'
чмок7 = 'https://media.tenor.com/images/ac05c51cc60ae6f73f746fc37c2f792f/tenor.gif'
чмок8 = 'https://media.tenor.com/images/d4f4a7a19c6560450d54561c6ebe55f0/tenor.gif'
#

class love(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.cog_name = ['любовь']

    @commands.command(
        aliases = ['обнять', 'Обнять', 'Hug'],
        description = 'обнять любого на сервере',
        usage = 'hug <@Ник>'
    )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def _hug(self, ctx, member: discord.Member):
         
        if member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name='Обнимашки:', value = f'**{ctx.author}** прости, но ты не можешь меня обнять(')
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name='Обнимашки:', value = f'**{ctx.author}**, нельзя обнимать самого себя ')
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        emb = discord.Embed(title = f'**Обнимашки!**',description = f'{ctx.author.mention} обнял(а) {member.mention}', color=0xFF0000)
        emb.set_image(url = random.choice([kek,lol,rfr,tgt,yhy,uju,img5,img6,img7,img8,img9,img10,img11,img12,img13,img14,img15,img16,img17,img18])) 
        emb.set_footer(text=f'Вызвано: {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
        await ctx.send(embed=emb)

    @_hug.error
    async def _hug_error(self, ctx, error):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Обнять:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb)
        if isinstance(error, commands.BadArgument):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Обнять:', value = 'Пользователь не найден!', inline = False)
            await ctx.send( embed = emb )
 
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Обнять:', value = 'Использование команды: `обнять [пользователь]`' )
            await ctx.send( embed = emb)    

    @commands.command(
        aliases = ['поцеловать'],
        description = 'поцеловать любого на сервере',
        usage = 'поцеловать <@Ник>'
    )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def чмок(self, ctx, member: discord.Member):
        
        if member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name='Поцелуй:', value = f'**{ctx.author}** прости, но ты не можешь меня поцеловать, а так хотелось(')
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name='Обнимашки:', value = f'**{ctx.author}**, нельзя поцеловать самого себя ')
            await ctx.send(embed=emb, delete_after=30)
 
            return

        emb = discord.Embed(title = f'**Целовашки!**',description = f'{ctx.author.mention} поцеловал(а) {member.mention}', color=0xFF0000)
        emb.set_image(url = random.choice([чмок1, чмок2, чмок3, чмок4, чмок5, чмок6, чмок7, чмок8])) 
        emb.set_footer(text=f'Вызвано: {ctx.message.author}',icon_url=ctx.message.author.avatar_url) 
        await ctx.send(embed=emb)   

    @чмок.error
    async def чмок_error(self, ctx, error):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Поцеловать:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb)
        if isinstance(error, commands.BadArgument):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Поцеловать:', value = 'Пользователь не найден!', inline = False)
            await ctx.send( embed = emb )
 
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Поцеловать:', value = 'Использование команды: `поцеловать [пользователь]`' )
            await ctx.send( embed = emb)       

def setup(client):
    client.add_cog(love(client))