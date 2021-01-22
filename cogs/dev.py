import discord
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

from module.catdivamodule import config

COPYRIGHT_TEXT = config.COPYRIGHT_TEXT
COPYRIGHT_TEXT_ERROR = config.COPYRIGHT_TEXT_ERROR
ICON = config.COPYRIGHT_ICON

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
**Версия бота: 3.0.0**

``В этом обновление было добавленно много нового и переделано тоже. С версии 3.0.0 разработка будет выходить хоть в раз месяц, но выход исправлений будут выходить с поступлением багов от вас``.

**Изменения:** 
``Полностью переработанные выводы ошибок, а также хелп притерпел изменения``   
	
**Добавленно:**
По факту кроме изменения оформления ничего)

**Убранно:**
``Зимние оформление d.хелп``
``Команда d.новыйгод``
			''')
		emb = discord.Embed(colour=discord.Color.red())
		emb.set_footer(text=COPYRIGHT_TEXT, icon_url = ICON)
		await ctx.send(embed=emb)

	@commands.command()
	async def приглаш(self, ctx):
		await ctx.send('``https://discord.com/oauth2/authorize?client_id=737324393117778020&scope=bot&permissions=1366617175``')
		
	@commands.command()
	async def тест_ошибок(self, ctx):
		await ctx.send(f'<**Ошибка**📤>:\nПоявилась ошибка в команде: ``тест_ошибок``\nПричина ошибки: Тест ')
		emb = discord.Embed(colour=discord.Color.red())
		emb.set_footer(text = COPYRIGHT_TEXT_ERROR, icon_url= ICON)
		await ctx.send(embed=emb)


def setup(client):
	client.add_cog(dev(client))