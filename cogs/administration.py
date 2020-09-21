import discord
from discord.ext import commands
from discord.utils import get
import os 
import datetime
import time

class administration(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Для администрации"]

    @commands.command(
		aliases=['очистить', 'clear'],
        description='удалить сообщения',
        usage='clear <число сообщений>'
	)
    @commands.has_permissions( administrator = True) 
    async def _clear( self, ctx, amount : int ):
	    await ctx.channel.purge( limit = amount )

	    await ctx.send(f'``✔️Удаленно {amount} сообщений``')
	    await ctx.channel.purge( limit = 1) 

    @commands.command(
		aliases=['кик', 'kick'],
        description='выгнать человека с сервера',
        usage='kick <@ник>'
	)
    @commands.has_permissions( administrator = True)
    async def _kick( self, ctx, member: discord.Member, *, reason = None ):
	    await ctx.channel.purge( limit = 1)

	    await member.kick( reason = reason )
	    await ctx.message( f'Был кикнут {member.mention}')

    @commands.command( 
		aliases=['бан', 'забанить', 'ban'],
        description='забанить человека на сервере',
        usage='ban <@ник>'
	)
    @commands.has_permissions( administrator = True)
    async def _ban(self, ctx, member: discord.Member, *, reason = None):
	    await ctx.channel.purge( limit = 1)

	    await member.ban( reason = reason)
	    await ctx.send(f'Был заблокирован {member.mention}')

    @commands.command( 
		aliases=['разбанить', 'анбан', 'unban'],
        description='рабанить человека на сервере',
        usage='unban <@ник>'
	)
    @commands.has_permissions( administrator = True)
    async def _unban ( self, ctx, *, member):
	    await ctx.channel.purge( limit = 1)
	    banned_users = await ctx.guild.bans()

	    for ban_entry in banned_users:
		    user = ban_entry.user # User#1234

		    await ctx.guild.unban( user )
		    await ctx.send( f'Был разблокирован { user.mention}' )

		    return     

def setup(client):
    client.add_cog(administration(client)) 