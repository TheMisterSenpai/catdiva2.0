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
			Полностью новые команды для администрации(Спасибо [𝓐𝓟] 𝓢𝓹𝓻𝓲𝓷𝓽𝓑𝓸𝓸𝓴#7792 за помощь)
			''')

	@commands.command(
		alliases = ['состояние']
	)		
	async def status(self, ctx):
		await ctx.send('''
			**Версия бота: 2.7.32**
		**Состояние бота:** :green_square:
		**Состояние хостинга:** :orange_square:
		**В разработке:** twitch.py :sleeping:  
		**Исправленно:** новый вывод ошибок) :partying_face: 

		Примечание: над ботом работает один разработчик и тестер, так что если вы нашли ошибку или баг, отправьте d.bag <описание ошибки>
			''')

def setup(client):
    client.add_cog(dev(client))        