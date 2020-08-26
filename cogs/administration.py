import discord
from discord.ext import commands
from discord.utils import get
import os 

class administration(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions( administrator = True) 
    async def clear( self, ctx, amount : int ):
	    await ctx.channel.purge( limit = amount )

	    await ctx.send(f'``✔️Удаленно {amount} сообщений``')
	    await ctx.channel.purge( limit = 1) 

    @commands.command( pass_context = True)
    @commands.has_permissions( administrator = True)
    async def kick( self, ctx, member: discord.Member, *, reason = None ):
	    await ctx.channel.purge( limit = 1)

	    await member.kick( reason = reason )
	    await ctx.message( f'Был кикнут {member.mention}')

    @commands.command( pass_context = True)
    @commands.has_permissions( administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
	    await ctx.channel.purge( limit = 1)

	    await member.ban( reason = reason)
	    await ctx.send(f'Был заблокирован {member.mention}')

    @commands.command( pass_context = True)
    @commands.has_permissions( administrator = True)
    async def unban ( self, ctx, *, member):
	    await ctx.channel.purge( limit = 1)
	    banned_users = await ctx.guild.bans()

	    for ban_entry in banned_users:
		    user = ban_entry.user # User#1234

		    await ctx.guild.unban( user )
		    await ctx.send( f'Был разблокирован { user.mention}' )

		    return     

    @commands.command()
    @commands.has_role(743888850765479936)
    async def restart(self, ctx):
        await ctx.send('Рестарт бота!')
        os.system('python ./bot.py')
        await bot.logout()

    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен administration.py')       

def setup(client):
    client.add_cog(administration(client)) 