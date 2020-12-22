import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import os 
import datetime
import time

from module.catdivamodule import api

from pymongo import MongoClient

MONGO = api.MONGO

cluster = MongoClient(MONGO)
collection = cluster.catdivadb.settingreport

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

    @commands.command(
        aliases=['голосование', 'quickpoll'],
        description = 'устроить голосование',
        usage = 'голосование <текст>'
    )
    @commands.has_permissions( administrator = True) 
    async def poll(self, ctx, *, question=None):
        if question is None:
            embed = discord.Embed(title="Ошибка", description="Укажите тему голосования!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Голосование", description=f"{question}\n👍 - Да\n👎 - Нет", color=discord.Color.green())
            bruh = await ctx.send(embed=embed)
            await bruh.add_reaction("👍")
            await bruh.add_reaction("👎")   

    @commands.command(
        aliases=['жалоба', 'send-report']

    )
    async def report(self, ctx, member: discord.Member=None, *, reason=None):
        if not collection.find_one({"guild_id": ctx.guild.id}):
            embed = discord.Embed(title="Ошибка", description="Система жалоб на этом сервере не включена!\nЧтобы включить введите - `>report-channel <on/off> <channel>`", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if member is None:
                embed = discord.Embed(title="Ошибка", description="Укажите пользователя `>report <member> <reason>`", color=discord.Color.red())
                await ctx.send(embed=embed)
            elif reason is None:
                embed = discord.Embed(title="Ошибка", description="Укажите причину жалобы `>report <member> <reason>`", color=discord.Color.red())
                await ctx.send(embed=embed)
            elif member == ctx.author:
                embed = discord.Embed(title="Ошибка", description="Вы не можете отправить жалобу на себя", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                if ctx.message.attachments:
                    for i in ctx.message.attachments:
                        channelid = collection.find_one({"guild_id": ctx.guild.id})["channel_id"]
                        channel = ctx.guild.get_channel(channelid)
                        embed = discord.Embed(title="Жалоба", description="Жалоба была успешно отправлена в канал для жалоб!", color=discord.Color.green())
                        await ctx.send(embed=embed)
                        embed2 = discord.Embed(title="Новая Жалоба!", description=f"**Отправитель:** {ctx.author.mention}\n**Нарушитель:** {member.mention}\n**Причина:** {reason}", color=discord.Color.green())
                        embed2.set_image(url=i.url)
                        msg = await channel.send(embed=embed2)
                        await msg.add_reaction("✅")
                        await msg.add_reaction("❌")
                        break
                else:
                    channelid = collection.find_one({"guild_id": ctx.guild.id})["channel_id"]
                    channel = ctx.guild.get_channel(channelid)
                    embed = discord.Embed(title="Жалоба", description="Жалоба была успешно отправлена в канал для жалоб!", color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed2 = discord.Embed(title="Новая Жалоба!", description=f"**Отправитель:** {ctx.author.mention}\n**Нарушитель:** {member.mention}\n**Причина:** {reason}", color=discord.Color.green())
                    msg = await channel.send(embed=embed2)
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❌")                

def setup(client):
    client.add_cog(administration(client)) 