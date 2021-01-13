import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

class dev(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.cog_name = ['разработка']

	@commands.Cog.listener()
	async def on_ready(self):
		print('[]разработка был запущин[]')

	@commands.command()
	async def path(self, ctx):
		await ctx.send('''
			**Версия бота: 2.7.4**
		**Состояние бота:** :green_square:
		**Состояние хостинга:** :orange_square:
		**В разработке:** оповещение о стримах (25%) :sleeping:  
		**Исправленно:** d.хелп и d.команды единая команда, а также добавлена d.заставка, новая любовная команда и оптимизация бота :partying_face: 

		Примечание: над ботом работает один разработчик и тестер, так что если вы нашли ошибку или баг, отправьте d.bag <описание ошибки>
			''')

	@commands.command()
	async def приглаш(self, ctx):
		await ctx.send('``https://discord.com/oauth2/authorize?client_id=737324393117778020&scope=bot&permissions=1366617175``')

def setup(client):
	client.add_cog(dev(client))