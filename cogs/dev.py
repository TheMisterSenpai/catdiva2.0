import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

class dev(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.cog_name = ['разработка']

	@commands.command(
		alliases = ['path']
	)
	async def path(self, ctx):
		await ctx.send('''
			Фикс разных маленьких багов
			''')

	@commands.command(
		alliases = ['состояние']
	)		
	async def status(self, ctx):
		await ctx.send('''
			**Версия бота: 2.7.33**
		**Состояние бота:** :green_square:
		**Состояние хостинга:** :orange_square:
		**В разработке:** twitch.py :sleeping:  
		**Исправленно:** ничего) :partying_face: 

		Примечание: над ботом работает один разработчик и тестер, так что если вы нашли ошибку или баг, отправьте d.bag <описание ошибки>
			''')

def setup(client):
    client.add_cog(dev(client))        