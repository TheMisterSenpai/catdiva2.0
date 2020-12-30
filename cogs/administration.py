import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import os 
import datetime
import time
import json
import random

from module.catdivamodule import api

from pymongo import MongoClient

MONGO = api.MONGO

cluster = MongoClient(MONGO)
collection = cluster.catdivadb.settingreport

answer5 = ['Вы не можете выгнать пользователя с такой же ролью!', 'Ваши роли одинаковы, я не могу так сделать!', 'Вы не можете выгнать такого же модератора как и вы!']
answer4 = ['Это невозможно сделать, так как выгнать меня может только основатель сервера!', 'Это может сделать только основатель сервера', 'Так сделать невозможно!', 'Увы, меня нельзя так остранить...']
answer3 = ['У вас не хватает прав!', 'Его роль стоит выше вашей!', 'Это нельзя сделать!', 'Ваша роль менее значима, чем этого пользователя!']
answer2 = ['Ты быканул на основателя сервера, или мне показалось?', 'Что он такого плохого тебе сделал?', 'При всём уважении к тебе я так не могу сделать!', 'Ах если бы я так мог...', 'Я не буду этого делать!', 'Сорян, но не в моих это силах!']
answer = ['Самоубийство не приведёт ни к чему хорошему!', 'Напомню: суицид - не выход!', 'Увы, я не могу этого сделать!', 'Самоубийство - не выход!', 'Не надо к себе так относиться!', 'Я не сделаю этого!', 'Я не буду это делать!', 'Я не выполню это действие', 'Не заставляй меня это сделать!']

class administration(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["администрация"]
 
    @commands.command(
        aliases=['очистить', 'clear'],
        description='удалить сообщения',
        usage='clear <число сообщений>'
    )
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def _clean(self, ctx, amount : int):
        await ctx.message.delete()
        deleted = await ctx.channel.purge( limit = amount )
        emb = discord.Embed(colour=discord.Color.green())
        emb.add_field(name=':broom: Очистка:', value = f'очищено сообщений: {len(deleted)}' )
        await ctx.send( embed = emb, delete_after = 30 )
 
    @_clean.error
    async def _clear_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':broom: Очистка:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb ) 
        if isinstance( error, commands.BadArgument ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':broom: Очистка:', value = 'Укажите число!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':broom: Очистка:', value = 'Использование команды: `очистить [кол-во сообщений]`' )
            await ctx.send( embed = emb )
        if isinstance( error, commands.errors.MissingPermissions ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':broom: Очистка:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)
 
    @commands.command(
        aliases=['кик', 'kick'],
        description='выгнать человека с сервера',
        usage='kick <@ник><причина>'
    )
    @commands.has_permissions( kick_members = True )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def _kick(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
 
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
 
        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        emb = discord.Embed()
        emb.add_field(name=':leg: Кик:', value = f'Вы уверены, что хотите кикнуть `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':leg: Кик:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:
            if reason == None:
                try:
 
                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':leg: Кик:', value = f'Вы, `{member.name}` кикнуты с сервера `{ ctx.guild.name }`!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                    await member.send( embed = emb)
 
                    await member.kick(reason=reason)
                except:
                    success = False
                else:
                    success = True
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':leg: Кик:', value = f'`{member.name}` кикнут!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await ctx.send(embed=emb)
 
                return
            try:
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':leg: Кик:', value = f'Вы, `{member.name}` кикнуты с сервера `{ ctx.guild.name }`!', inline = False)
                emb.add_field( name = 'По причине:', value = reason, inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await member.send( embed = emb)
 
                await member.kick(reason=reason)
            except:
                success = False
            else:
                success = True
 
            emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':leg: Кик:', value = f'`{member.name}` кикнут!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
            await ctx.send(embed=emb)
 
    @_kick.error
    async def _kick_error(self, ctx, error):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Кик:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb)
        if isinstance(error, commands.BadArgument):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Кик:', value = 'Пользователь не найден!', inline = False)
            await ctx.send( embed = emb )
 
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Кик:', value = 'Использование команды: `кик [пользователь] <причина>`' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingPermissions ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Кик:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)    
 
    @commands.command(
        aliases=['бан', 'забанить', 'ban'],
        description='забанить человека на сервере',
        usage='ban <@ник><причина>'
    )
    @commands.has_permissions( kick_members = True )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def _ban(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.delete()
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':leg: Кик:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
 
        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':hammer: Бан:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)
 
            return
        emb = discord.Embed()
        emb.add_field(name=':hammer: Бан:', value = f'Вы уверены, что хотите забанить `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':hammer: Бан:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:
 
            if reason == None:
 
                try:
 
                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':hammer: Бан:', value = f'Вы, `{member.name}` забаннены на сервере `{ ctx.guild.name }`!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                    await member.send( embed = emb)
 
                    await member.ban(reason=None)
                except:
                    success = False
                else:
                    success = True
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':hammer: Бан:', value = f'Участник `{member.name}` забаннен!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
 
                await ctx.send(embed=emb)
 
                return
 
            try:
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':hammer: Бан:', value = f'Вы, `{member.name}` забаннены на сервере `{ ctx.guild.name }`!', inline = False)
                emb.add_field( name = 'По причине:', value = reason, inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await member.send( embed = emb)
 
                await member.ban(reason=reason)
            except:
                success = False
            else:
                success = True
 
            emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':hammer: Бан:', value = f'Участник `{member.name}` забаннен!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
 
            await ctx.send(embed=emb)
 
    @_ban.error
    async def _ban_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Бан:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.BadArgument ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Бан:', value = 'Вы указали что-то не то!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Бан:', value = 'Использование команды: `бан [пользователь] <причина>`' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingPermissions ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Бан:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)    
    
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

    @_unban.error
    async def _unban_error(self, ctx, error):
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Разбан:', value = 'Использование команды: `разбанить [пользователь] <причина>`' )
            await ctx.send( embed = emb, delete_after=30 )
        
        if isinstance( error, commands.errors.MissingPermissions ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Разбан:', value = 'У вас не хватает прав! \n❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' )
            await ctx.send( embed = emb)      
 
    @commands.command(
        aliases=['мут', 'mute'],
        description='замутить человека на сервере',
        usage='mute <@ник><время><причина>'
    )
    @commands.has_permissions( kick_members = True )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    async def _mute(self, ctx, member:discord.Member, duration=None, *, reason=None):
        await ctx.message.delete()
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мут:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
 
        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мут:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мут:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мут:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':shushing_face: Мут:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)
 
            return
        emb = discord.Embed()
        emb.add_field(name=':shushing_face: Мут:', value = f'Вы уверены, что хотите замутить `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':shushing_face: Мут:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:
 
            if duration == None:
                if reason == None:
                    try:
                        progress = await ctx.send('Мьючу пользователя!', delete_after = 5)
 
                        emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                        emb.add_field( name = ':shushing_face: Мут:', value = f'Участник `{member.name}` замучен!\nОн не выйдет из мута, пока его не размутят!', inline = False)
                        emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                        await ctx.send( embed = emb)
   
 
                        for channel in ctx.guild.text_channels:
                            await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
    
                        for channel in ctx.guild.voice_channels:
                            await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
                    except:
                        success = False
                    else:
                        success = True
 
                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':shushing_face: Мут:', value = f'Вы, `{member.name}` замучены на сервере `{ ctx.guild.name }`!\nВы не выйдете из мута, пока вас не размутят!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                    await member.send( embed = emb)
 
 
                    return
 
 
                try:
                    progress = await ctx.send('Мьючу пользователя!', delete_after = 5)
 
                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':shushing_face: Мут:', value = f'Участник `{member.name}` замучен!\nОн не выйдет из мута, пока его не размутят!', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                    await ctx.send( embed = emb)
  
 
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
   
                    for channel in ctx.guild.voice_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
                except:
                    success = False
                else:
                    success = True
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':shushing_face: Мут:', value = f'Вы, `{member.name}` замучены на сервере `{ ctx.guild.name }`!\nВы не выйдете из мута, пока вас не размутят!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await member.send( embed = emb)
 
                return
 
 
            unit = duration[-1]
            if unit == 'с':
                time = int(duration[:-1])
                longunit = 'секунд'
            elif unit == 's':
                time = int(duration[:-1])
                longunit = 'секунд'
            elif unit == 'м':
                time = int(duration[:-1]) * 60
                longunit = 'минуту/минут'
            elif unit == 'm':
                time = int(duration[:-1]) * 60
                longunit = 'минуту/минут'
            elif unit == 'ч':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'час/часов'
            elif unit == 'h':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'час/часов'
            elif unit == 'д':
                time = int(duration[:-1]) * 60 * 60 *24
                longunit = 'день/дней'
            elif unit == 'd':
                time = int(duration[:-1]) * 60 * 60 *24
                longunit = 'день/дней'
            else:
                await ctx.send('Неправильное написание времени!', delete_after = 30)
                return
 
            if reason == None:
                try:
                    progress = await ctx.send('Мьючу пользователя!', delete_after = 5)
 
                    emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                    emb.add_field( name = ':shushing_face: Мут:', value = f'Участник `{member.name}` замучен!\nОн выйдет из мута через: {str(duration[:-1])} {longunit}', inline = False)
                    emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                    await ctx.send( embed = emb)
 
  
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
 
                    for channel in ctx.guild.voice_channels:
                        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
                except:
                    success = False
                else:
                    success = True
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':shushing_face: Мут:', value = f'Вы, `{member.name}` замучены на сервере `{ ctx.guild.name }`!\nВы выйдете из мута через: {str(duration[:-1])} {longunit}', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await member.send( embed = emb)
    
                await asyncio.sleep(time)
                try:
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(member, overwrite=None, reason=reason)
                except:
                    pass
 
                return
  
            try:
                progress = await ctx.send('Мьючу пользователя!', delete_after = 5)
 
                emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':shushing_face: Мут:', value = f'Участник `{member.name}` замучен!\nОн выйдет из мута через: {str(duration[:-1])} {longunit}', inline = False)
                emb.add_field( name = 'По причине:', value = reason, inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await ctx.send( embed = emb)
 
 
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)
 
                for channel in ctx.guild.voice_channels:
                    await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
            except:
                success = False
            else:
                success = True
 
            emb = discord.Embed( colour = discord.Color.red(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':shushing_face: Мут:', value = f'Вы, `{member.name}` замучены на сервере `{ ctx.guild.name }`!\nВы выйдете из мута через: {str(duration[:-1])} {longunit}', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
  
            await member.send( embed = emb)
    
            await asyncio.sleep(time)
            try:
                for channel in ctx.guild.channels:
                    await channel.set_permissions(member, overwrite=None, reason=reason)
            except:
                pass
 
 
    @_mute.error
    async def _mute_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Мут:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.BadArgument ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Мут:', value = 'Вы что-то указали не то!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Мут:', value = 'Использование команды: `мут [пользователь] <время> <причина>`' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingPermissions ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Мут:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)    
        
    @commands.command(
        aliases=['размут'],
        description='размутить человека на сервере',
        usage='unmute <@ник>'
    )
    @commands.cooldown(1, per = 10, type = discord.ext.commands.BucketType.guild )
    @commands.has_permissions( kick_members = True )
    async def _unmute(self, ctx, member:discord.Member, *, reason=None):
        await ctx.message.delete()
 
        if ctx.author.top_role == member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размут:', value = random.choice(answer5))
            await ctx.send(embed=emb, delete_after=30)
 
            return
        elif member == ctx.bot.user:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размут:', value = random.choice(answer4))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif ctx.author.top_role < member.top_role:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размут:', value = random.choice(answer3))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.author:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размут:', value = random.choice(answer))
            await ctx.send(embed=emb, delete_after=30)
 
            return
 
        elif member == ctx.guild.owner:
            emb = discord.Embed(colour=discord.Color.red())
            emb.add_field(name=':smiley: Размут:', value = random.choice(answer2))
            await ctx.send(embed=emb, delete_after=30)
 
            return
        emb = discord.Embed()
        emb.add_field(name=':smiley: Размут:', value = f'Вы уверены, что хотите размутить `{member.name}`?')
        emb.set_footer(text='Не нажимайте на галочку, если это ошибка!')
        msg = await ctx.send(embed=emb, delete_after = 30)
        await msg.add_reaction('✅')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '✅'
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check = check)
        except asyncio.TimeoutError:
            emb = discord.Embed(colour=discord.Color.green())
            emb.add_field(name=':smiley: Размут:', value = 'Действие отменнено!')
            await ctx.send(embed = emb, delete_after=30 )
        else:
            await ctx.send('Размучиваю пользователя', delete_after = 5)
            try:
                for channel in ctx.message.guild.channels:
                    await channel.set_permissions(member, overwrite=None, reason=reason)
            except:
                success = False
            else:
                success = True
 
            if reason == None:
                emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':smiley: Размут:', value = f'Вы, `{member.name}` размучены на сервере `{ ctx.guild.name }`!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
 
                await member.send( embed = emb)
            
                emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
                emb.add_field( name = ':smiley: Размут:', value = f'Участник `{member.name}` размучен!', inline = False)
                emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
                await ctx.send( embed = emb)
 
                return
 
            emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':smiley: Размут:', value = f'Вы, `{member.name}` размучены на сервере `{ ctx.guild.name }`!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
  
            await member.send( embed = emb)
            
            emb = discord.Embed( colour = discord.Color.green(), timestamp = ctx.message.created_at)
            emb.add_field( name = ':smiley: Размут:', value = f'Участник `{member.name}` размучен!', inline = False)
            emb.add_field( name = 'По причине:', value = reason, inline = False)
            emb.add_field( name = 'Модератор:', value = f'{ctx.author}')
            await ctx.send( embed = emb)
 
    @_unmute.error
    async def _unmute_error( self, ctx, error ):
        if isinstance( error, commands.CommandOnCooldown):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Размут:', value = 'Подождите 10 секунд перед повторным использованием!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.BadArgument ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Размут:', value = 'Вы указали что-то не то!' )
            await ctx.send( embed = emb )
        if isinstance( error, commands.errors.MissingRequiredArgument ):
            emb = discord.Embed()
            emb.add_field( name = ':x: Размут:', value = 'Использование команды: `размут [пользователь] <причина>`' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.MissingPermissions ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = ':x: Размут:', value = 'У вас не хватает прав!' )
            await ctx.send( embed = emb)
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)    

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

    @poll.error
    async def poll_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)
            
    @commands.command(
        aliases=['жалоба', 'send-report'],
        description = 'пожаловаться на человека',
        usage = 'жалоба <@ник><жалоба>'
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

    @report.error
    async def report_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)                                                  

def setup(client):
    client.add_cog(administration(client)) 