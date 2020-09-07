import discord
from discord.ext import commands
from discord.utils import get
import os 
import datetime
import time

from contextlib import closing
import sqlite3
from Utils import DB

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

    @commands.command(aliases=['adduser'])
    @commands.has_permissions( administrator = True)
    async def __adduser (self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("укажите участника")
        else:
            conn = sqlite3.connect('./Data/DataBase/warn_users.db')
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            warns INT,
            id INT
    )""")

            if cursor.execute(f"SELECT id FROM users where id = {member.id}").fetchone() is None:
                    cursor.execute(
                        f"INSERT INTO users VALUES('{member.id}, 0)"
                        )
                    conn.commit()
                    await ctx.message.add_reaction(':white_check_mark:')
            else:
                await ctx.send('он уже есть в бд')

    @commands.command()
    @commands.has_permissions( administrator = True) 
    async def warn(self, ctx, member: discord.Member = None, *, reason = None):  
        global Warnings 
        
        await ctx.message.delete()

        if not member:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Правильное использование команды: `warn @пользователь причина`', color=0x800080))
        if member.id == ctx.guild.owner.id:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Данный пользователь, {member.mention}, является создателем этого сервера!**', color=0x800080))
        if member.id == ctx.guild.me.id:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Я не могу заварнить самого себя!**', color=0x800080))
        if ctx.author.top_role.position < member.top_role.position:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Эм... Это троллинг? Ты не можешь заварнить человека с позицией выше твоей!**', color=0x800080))
        if member.id == ctx.author.id:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Напомню, суицид - это не выход!**', color=0x800080))
        if member.top_role > ctx.guild.me.top_role:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Я не могу заварнить {member.mention}, так как его роль выше моей!**', color=0x800080))
            warnings = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
        
        if warnings == '2':
            cursor.execute(f"UPDATE users SET warns = {0} WHERE id = {member.id}")
            conn.commit()
            for i in member.roles:
                await member.remove_roles(i)
            if reason is None:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: Пользователь {member.mention} получил 3/3 варнов и все его роли были сняты!\n Причина варна: Не указана**', color=0x800080))
            else:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: Пользователь {member.mention} получил 3/3 варнов и все его роли были сняты!\n Причина варна: {reason}**', color=0x800080))
        else:
            cursor.execute(f"UPDATE users SET warns = warns + {1} WHERE id = {member.id}")
            conn.commit()
            warnings2 = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
            if reason is None:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: Пользователь {member.mention} получил варн. \n Причина варна: Не указана \n Всего варнов у него: {warnings2}!**', color=0x800080))
            else:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: Пользователь {member.mention} получил варн. \n Причина варна: {reason} \n Всего варнов у него: {warnings2}!**', color=0x800080))
        emb = discord.Embed(title = 'Варн', colour = discord.Color.red())
        now_date = datetime.datetime.now()
        emb.set_author(name = member.name, icon_url = member.avatar_url)
        emb.add_field(name = '__***Выдал:***__', value = '{}'.format(ctx.author.display_name), inline = False)
        emb.add_field(name = '__***Тип наказания:***__', value = 'warn', inline = False)
        emb.add_field(name = '__***Количество:***__', value = '{}'.format(warnings), inline = False)
        emb.add_field(name = '__***Время выдачи:***__', value = '{}'.format(now_date), inline = False)
        if reason is None:
            emb.add_field(name = '__***Причина:***__', value = 'Не указана.', inline = False)
        else:
            emb.add_field(name = '__***Причина:***__', value = '{}'.format(reason), inline = False)
        emb.set_footer(text = 'Не отвечайте на это сообщение.', icon_url = ctx.author.avatar_url)
        await member.send(embed = emb) 

    @commands.command()
    @commands.has_permissions( administrator = True)
    async def unwarn(self, ctx, member: discord.Member = None, *, reason = None):
        global Warnings
        
        await ctx.message.delete()

        if not member:
            return await ctx.send(embed = discord.Embed(description = f'**:warning: Правильное использование команды: `unwarn @пользователь причина`', color=0x800080))
            warnings = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
        if warnings == '0':
            return await ctx.send(embed = discord.Embed(description = f'**:warning: У пользователя {member.mention} 0 варнов, снять варн не возможно!', color=0x800080))
        else:
            if not member:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: Правильное использование команды: `unwarn @пользователь причина`', color=0x800080))
        warnings = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
        
        if warnings == '0':
            return await ctx.send(embed = discord.Embed(description = f'**:warning: У пользователя {member.mention} 0 варнов, снять варн не возможно!', color=0x800080))
        else:
            cursor.execute(f"UPDATE users SET warns = warns - {1} WHERE id = {member.id}")
            conn.commit()
            warnings2 = cursor.execute(f"SELECT warns FROM users WHERE id = {member.id}").fetchone()[0]
            if reason is None:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: У пользователя {member.mention} был снят варн. \n Причина снятия: Не указана \n Всего варнов у него: {warnings2}!**', color=0x800080))
            else:
                return await ctx.send(embed = discord.Embed(description = f'**:warning: У пользователя {member.mention} был снят варн. \n Причина снятия: {reason} \n Всего варнов у него: {warnings2}!**', color=0x800080))
        emb = discord.Embed(title = 'Варн', colour = discord.Color.red())
        now_date = datetime.datetime.now()
        emb.set_author(name = member.name, icon_url = member.avatar_url)
        emb.add_field(name = '__***Выдал:***__', value = '{}'.format(ctx.author.display_name), inline = False)
        emb.add_field(name = '__***Тип наказания:***__', value = 'unwarn', inline = False)
        emb.add_field(name = '__***Количество:***__', value = '{}'.format(warnings), inline = False)
        emb.add_field(name = '__***Время выдачи:***__', value = '{}'.format(now_date), inline = False)
        if reason is None:
            emb.add_field(name = '__***Причина:***__', value = 'Не указана.', inline = False)
        else:
            emb.add_field(name = '__***Причина:***__', value = '{}'.format(reason), inline = False)
        emb.set_footer(text = 'Не отвечайте на это сообщение.', icon_url = ctx.author.avatar_url)
        await member.send(embed = emb)

    @commands.command()
    @commands.has_permissions( administrator = True)   
    async def warns(self, ctx, member: discord.Member = None):
        if member is None: # если не указан пользователь
            await ctx.send(embed = discord.Embed(description = f'У **{ctx.author}** {cursor.execute("SELECT warns FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} предупреждений (варнов)')) # выводим из таблицы users столбец warns и получаем предупреждение которые есть у вас
        else: #иначе
            await ctx.send(embed = discord.Embed(description = f'У **{member}** {cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]} предупреждений (варнов)')) # выводит из таблицы users данные столбца warns и получаем предупреждение которые есть у мембера, которого вы отмечаете в сообщении 

def setup(client):
    client.add_cog(administration(client)) 