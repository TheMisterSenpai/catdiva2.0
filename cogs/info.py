import discord
from discord.ext import commands
from discord.utils import get
import asyncio

class info(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Информация", True]

    @commands.command(
        aliases = ['инфо', 'info'],
        description='узнать о боте',
        usage='.info'
    )
    async def info(self, ctx):
        await ctx.send('**Привет, меня зовут Кошка Дива и я офицальный бот сервера "Убежище клоунов"**')
        await asyncio.sleep(5)
        await ctx.send('**Чтоб посмотреть все мои команды, просто напиши .help**')
        await asyncio.sleep(3)
        await ctx.send('**Для команд администраторов напиши .ad_help**')
        await asyncio.sleep(5)
        await ctx.send('**Для экономики напиши .ec_help**')
        await asyncio.sleep(5)
        await ctx.send('**Если вы нашли баг или недоработку то напишите .bag или пишите моему разработчику** @TheMisterSenpai#2033')
        await asyncio.sleep(5)
        await ctx.send('**Мой исходный код: https://github.com/TheMisterSenpai/catdiva2.0 **')

    @commands.command(
        aliases=['сервер', 'серверинфо'],
        description="Информация о сервере",
        usage='.server'
    )
    async def server(self, ctx):
 
        members = ctx.guild.members
        bots = len([m for m in members if m.bot])
        users = len(members) - bots
        online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
        offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
        idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
        dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
        allvoice = len(ctx.guild.voice_channels)
        alltext = len(ctx.guild.text_channels)
        allroles = len(ctx.guild.roles)
 
        embed = discord.Embed(title=f"{ctx.guild.name}", color= 302112 , timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.guild.icon_url)
 
        embed.add_field(name=f"Пользователей", value=f"Участников: **{users}**\n"
                                                f"Ботов: **{bots}**\n"
                                                f"Онлайн: **{online}**\n"
                                                f"Отошёл: **{idle}**\n"
                                                f"Не Беспокоить: **{dnd}**\n"
                                                f"Оффлайн: **{offline}**")
 
        embed.add_field(name=f"Каналов", value=f"Голосовые: **{allvoice}**\n"
                                            f"Текстовые: **{alltext}**\n")
 
        embed.add_field(name=f"Уровень Буста", value=f"{ctx.guild.premium_tier} (Бустеров: {ctx.guild.premium_subscription_count})")
        embed.add_field(name=f"Количество Ролей", value=f"{allroles}")
        embed.add_field(name=f"Создатель сервера", value=f"{ctx.guild.owner}")
        embed.add_field(name=f"Регион сервера", value=f"{ctx.guild.region}")
        embed.add_field(name=f"Дата создания сервера", value=f"{ctx.guild.created_at.strftime('%b %#d %Y')}")
 
        embed.set_footer(text='Вызвал команду: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
  

def setup(client):
    client.add_cog(info(client)) 