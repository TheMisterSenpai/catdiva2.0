import discord
from discord.ext import commands
from discord.utils import get
from config import PREFIX

class command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
        self.cog_name = ["команды"]

    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed( title = '📗Навигация по командам бота📗')

        emb.add_field( name = '{}report'.format( PREFIX ), value = '🚬пожаловаться на нарушителя')
        emb.add_field( name = '{}wiki'.format( PREFIX ), value = '🔎поиск информации на Wikpedia')
        emb.add_field( name = '{}userinfo'.format( PREFIX ), value = '📡узнать про себя на сервере')
        emb.add_field( name = '{}send_l'.format( PREFIX ), value = '✉️Отправка личных сообщений')	
        emb.add_field( name = '{}phone_info'.format( PREFIX ), value = '📱узнать местонахождения человека по номеру(В научных целях)')
        emb.add_field( name = '{}хентай'.format( PREFIX ), value = '🍓интересные картинки и гифки')    
        emb.add_field( name = '{}server'.format( PREFIX ), value = 'узнать информацию о сервере') 

        await ctx.send( embed = emb )

    @commands.command()
    async def ad_help(self, ctx): 
        emb = discord.Embed( title = '📗Навигация по командам бота для администрации📗')

        emb.add_field( name = '{}clear'.format( PREFIX ), value = '🌪Очистка сообщений ')
        emb.add_field( name = '{}kick'.format( PREFIX ), value = '🐷удаления со сервера ')
        emb.add_field( name = '{}ban'.format( PREFIX ), value = '🙅‍блокировка на сервере')
        emb.add_field( name = '{}unban'.format( PREFIX ), value = '👌разблокировка на сервере ')

        await ctx.send( embed = emb ) 

    @commands.command()
    async def ec_help(self, ctx): 
        emb = discord.Embed( title = '📗Навигация по командам бота для экономики📗')

        emb.add_field( name = '{}timely'.format( PREFIX ), value = '💸получить на баланс 350 стонксов')
        emb.add_field( name = '{}balance'.format( PREFIX ), value = '💳посмотреть баланс')
        emb.add_field( name = '{}shop'.format( PREFIX ), value = '💰магазин')
        emb.add_field( name = '{}addshop'.format( PREFIX ), value = '☑️добавить роль в магазин(команда @роль цена)')
        emb.add_field( name = '{}removeshop'.format( PREFIX ), value = '❌удалить роль из магазина(команда @роль)')
        emb.add_field( name = '{}buy'.format( PREFIX ), value = '💎купить роль из магазина(команда @роль)')
        emb.add_field( name = '{}give'.format( PREFIX ), value = '💌подарить любому деньги(команда @ник сумма)')

        await ctx.send( embed = emb )



def setup(client):
    client.add_cog(command(client)) 