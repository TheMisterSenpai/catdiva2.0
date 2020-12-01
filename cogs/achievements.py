import discord
from discord.ext import commands
from discord.utils import get


class achievements(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Достижения", True]

#СКОРО
    @commands.command(
        aliases = ['разработчик']
    )
    @commands.is_owner()
    async def dev(self, ctx):
        await ctx.send(f'{ctx.author} получил достижение **разработчик**')
        owner_role = discord.utils.get(ctx.message.guild.roles, name = 'разработчик бота')
        if owner_role in ctx.author.roles:
            await ctx.send(embed = discord.Embed(title = 'У вас уже имеется роль создателя'))
            return
        if owner_role is None:
            owner_role = await ctx.guild.create_role(name = 'разработчик бота', permissions = discord.Permissions( administrator = True), color = discord.Color.blurple())
        await ctx.author.add_roles(owner_role, reason = None, atomic = True)
    
    @dev.error
    async def dev_error( ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(embed = discord.Embed(title = '`Вы не являетесь моим создателем!`', color = discord.Color.dark_red()))
        

    @commands.command(
        aliases = ['первопроходец']
    )
    async def first(self, ctx):
        await ctx.send(f'{ctx.author} получил достижение **первопроходец**')
        owner_role = discord.utils.get(ctx.message.guild.roles, name = 'первопроходец')
        if owner_role in ctx.author.roles:
            await ctx.send(embed = discord.Embed(title = 'вы уже получили достижение **первопроходец**'))
            return
        if owner_role is None:
            await ctx.guild.create_role(name = 'первопроходец', permissions = discord.Permissions(), color = discord.Color.blurple())    
        await ctx.author.add_roles(owner_role, reason = None, atomic = True) 
    '''    
    @commands.command(
        aliases = ['хэллоуин']
    )
    async def hn(self, ctx):
        await ctx.send(f'{ctx.author} получил достижение **хэллоуин 2020**')
        owner_role = discord.utils.get(ctx.message.guild.roles, name = '🎃')
        if owner_role in ctx.author.roles:
            await ctx.send(embed = discord.Embed(title = 'вы уже получили достижение **хэллоуин 2020**'))
            return
        if owner_role is None:
            await ctx.guild.create_role(name = '🎃', permissions = discord.Permissions(), color = discord.Color.blurple())    
        await ctx.author.add_roles(owner_role, reason = None, atomic = True)       
    '''

    @commands.command(
        aliases = ['новыйгод']
    )
    async def newyear(self, ctx):
        await ctx.send(f'{ctx.author} получил достижение **❄Новый год 2021❄**')
        owner_role = discord.utils.get(ctx.message.guild.roles, name = '❄Новый год 2021❄')
        if owner_role in ctx.author.roles:
            await ctx.send(embed = discord.Embed(title = 'вы уже получили достижение **❄Новый год 2021❄**'))
            return
        if owner_role is None:
            await ctx.guild.create_role(name = '❄Новый год 2021❄', permissions = discord.Permissions(), color = discord.Color.blurple())    
        await ctx.author.add_roles(owner_role, reason = None, atomic = True) 
    
def setup(client):
    client.add_cog(achievements(client)) 