import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import os 
import datetime
import time


class administration(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["администрация"]

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
  
    @commands.command(
        aliases=['мут', 'mute'],
        description='замутить человека на сервере',
        usage='mute <@ник> <время>'
    )
    @commands.has_permissions( administrator = True)
    async def _mute(self, ctx, member:discord.Member, duration, *, reason=None):
        unit = duration[-1]
        print(f'{unit}')
        if unit == 'с':
            time = int(duration[:-1])
            longunit = 'секунд'
        elif unit == 'м':
            time = int(duration[:-1]) * 60
            longunit = 'минут'
        elif unit == 'ч':
            time = int(duration[:-1]) * 60 * 60
            longunit = 'часов'
        else:
            await ctx.send('Неправильно! Пиши `c`, `м`, `ч`')
            return

        progress = await ctx.send('Пользователь теперь замучен!')
        try:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)

            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
        except:
            success = False
        else:
            success = True

        await ctx.send(f'{member} замучен на {duration}')
        await asyncio.sleep(time)
        try:
            for channel in ctx.guild.channels:
                 await channel.set_permissions(member, overwrite=None, reason=reason)
        except:
            pass

def setup(client):
    client.add_cog(administration(client)) 