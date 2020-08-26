import discord
from discord.ext import commands
from discord.utils import get

class info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        aliases=['сервер', 'серверинфо'],
        description="Информация о сервере")
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

    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен info.py')    

def setup(client):
    client.add_cog(info(client)) 