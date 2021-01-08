'''
Создатель бота: TheMisterSenpai@6701
Переводчик: бабабуй#2001
Тестеры: бабабуй#2001, [𝓐𝓟] 𝓢𝓹𝓻𝓲𝓷𝓽𝓑𝓸𝓸𝓴#7792, Latr0pket#4364, gGorr#3954


Пригласить бота к себе на сервер: https://discord.com/api/oauth2/authorize?client_id=737324393117778020&permissions=8&scope=bot

Мой сервер - https://discord.gg/aZfHSjR

Убидительная просьба, если вы берёте моего бота как за основу, то указывайте на этот гитхаб


Все права защищены | TheMisterSenpai
'''
import discord
import os
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
from discord import Streaming

import json
from module.catdivamodule import config
from module.catdivamodule import api
import nest_asyncio
from pymongo import MongoClient

from module.catdivamodule.loops import Loop
from colorama import Fore, Style
from colorama import init 

from module.cybernetic.paginator import Paginator as pr

MONGO = api.MONGO

cluster = MongoClient(MONGO)
collection = cluster.catdivadb.prefixsett

STATUS = config.STATUS
STATUSURL = config.STATUSURL
COLOR_ERROR = config.COLOR_ERROR
COPYRIGHT_TEXT_ERROR = config.COPYRIGHT_TEXT_ERROR
COPYRIGHT_ICON = config.COPYRIGHT_ICON

def get_prefix_gg(client, message):
    prefix_server = collection.find_one({"guild_id": message.guild.id})["prefix"]
    return str(prefix_server)

client = commands.Bot( command_prefix =  get_prefix_gg )
client.remove_command('help')
init()

#START bot
# Запуск Бота
@client.event
async def on_ready():
    print(" ")
    print(Fore.CYAN + "===================================" + Style.RESET_ALL)
    print(
        Fore.CYAN + '|' + Style.RESET_ALL + f' Смена статуса на стандартный... ' + Fore.CYAN + '|' + Style.RESET_ALL)
    await client.change_presence(activity=discord.Streaming(name=STATUS, url=STATUSURL))
    print(
        Fore.CYAN + '|' + Style.RESET_ALL + f'        Бот активирован!         ' + Fore.CYAN + '|' + Style.RESET_ALL)
    print(Fore.CYAN + "===================================" + Style.RESET_ALL)
    print(f'  Статус   - {STATUS}          ')
    print(f'  Имя бота - {client.user.name}')
    print(f'  ID бота  - {client.user.id}  ')
    print(Fore.CYAN + "===================================" + Style.RESET_ALL)
    print(" ")

    loop = Loop(client)
    try:
        loop.activator()
    except AssertionError:
        pass

    for guild in client.guilds:
        post = {
            "guild_id": guild.id,
            "prefix": "d."
        }
        if collection.count_documents({"guild_id": guild.id}) == 0:
            collection.insert_one(post)
        else:
            pass              
#
#Error
@client.event
async def on_command_error(ctx, error):
    print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Команда: {ctx.message.content}")
    print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Сервер:  {ctx.message.guild}")
    print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Ошибка:  {error}")
#
@client.event       
async def on_member_join( member ):  
    role = discord.utils.get( member.guild.roles, id = 761927608442552320 )
    await member.add_roles( role ) 

#
#cogs
@client.command()
async def load(ctx, extensions):
    if ctx.author.id == 364437278728388611:
        client.load_extension(f'cogs.{extensions}')
        await ctx.send(f'**Был загружен** {extensions}')
    else:
        await ctx.send(f'Вы не создатель {ctx.author}')

@client.command()
async def reload(ctx, extensions):
    if ctx.author.id == 364437278728388611:
        client.unload_extension(f'cogs.{extensions}')
        client.load_extension(f'cogs.{extensions}')
        await ctx.send(f'**Был перезапущен** {extensions}')
    else:
        await ctx.send(f'Вы не создатель {ctx.author}')

@client.command()
async def unload(ctx, extensions):
    if ctx.author.id == 364437278728388611:
        client.unload_extension(f'cogs.{extensions}')
        await ctx.send(f'**Был отключен** {extensions}')
    else:
        await ctx.send(f'Вы не создатель {ctx.author}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
#
#send me
@client.event
async def on_guild_join( guild ):


    me = client.get_user(364437278728388611)

    emb = discord.Embed( title = f'Я пришел на новый сервер!' )
    for guild in client.guilds:
        category = guild.categories[0]
        try:
            channel = category.text_channels[0]
        except:
            channel = category.voice_channels[0]
        link = await channel.create_invite()
    emb.add_field( name = guild.name, value = f"Участников: {len(guild.members)}\nСсылка: {link}" )

    
    await me.send( embed = emb )            
#bag
@client.command()
async def bag(ctx, *, bag ):
    message = ctx.message
    channel = client.get_channel( 749869477419810836) 
        
    embed = discord.Embed(
        title = 'Баг отправлен!',
        description = f'Баг: {bag}',
        color = 0x508C31
    )
    await ctx.send(
        embed = embed
    )   
    await channel.send(
        f'**{ctx.author}** отправил баг: {bag}'
    )
#
#ping
@client.command()
async def ping(ctx):
    ping = client.latency
    ping_emoji = "🟩🔳🔳🔳🔳"
    
    ping_list = [
        {"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
        {"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
        {"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
        {"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
        {"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
        {"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}]
    
    for ping_one in ping_list:
        if ping > ping_one["ping"]:
            ping_emoji = ping_one["emoji"]
            break

    message = await ctx.send("Пожалуйста, подождите. . .")
    await message.edit(content = f"*Пинг бота*: {ping_emoji} `{ping * 1000:.0f}ms` ") 
#
#Private
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel.id == 715275220981907488:
        for guild in client.guilds:
            if guild.id == 669193966641741884:
                mainCategory = discord.utils.get(guild.categories, id= 715275155861143652)
                channel2 = await guild.create_voice_channel(name=f"{member.display_name}",category=mainCategory)
                print('[log]Создан голосовой чат')
                await member.move_to(channel2)
                await channel2.set_permissions(member, manage_channels = True)
                def check(a,b,c):
                    return len(channel2.members) == 0
                await client.wait_for('voice_state_update', check=check)
                await channel2.delete()
                print('[log]Удален голосовой чат')
#
#Защита от спама
@client.event
async def on_message(message): #trouble-free 24/7 event
    try:
        try:
            if isinstance(message.channel, discord.DMChannel): #check on DM channel
                return
        except AttributeError:
            return
        await client.process_commands(message) #continuation of command execution in case of on_message event
    except TypeError:
        return     

#настройки
@client.command()
async def настройки(ctx):
    prefix = collection.find_one({"guild_id": ctx.guild.id})["prefix"]

    embed1 = discord.Embed(title = 'Настройки сервера',
        description = 'Если вы не знаете как настроить ваш сервер и меня, то вам помогу. Нажмите на ➡ чтоб начать настройку')
    embed2 = discord.Embed(title = 'Жалобы',
        description = f'Настройте команду жалобы. Просто пропишите {prefix}канал-жалоб on/off #ваш канал')
    embed3 = discord.Embed(title = 'Смена префикса',
        description = f'Смени префикс бота для сервера через команду {prefix}префикс (ваш префикс)')
    embed4 = discord.Embed(title = 'Оповещение о стримах на twitch',
        description = f'**Пока не доступно**')

    embeds = [embed1, embed2, embed3, embed4]
    message = await ctx.send(embed = embed1)
    page = pr(client, message, only = ctx.author, use_more = False, embeds = embeds)
    await page.start()

#prefix
@client.event
async def on_guild_join(guild):
    post = {
        "guild_id": guild.id,
        "prefix": "d."
    }
    
    collection.insert_one(post)  

# Когда бота удалят с сервера
 
@client.event
async def on_guild_remove(guild):
    collection.delete_one({"guild_id": guild.id})
 
# Смена префикса
 
@client.command(aliases=['префикс', 'prefix'])
@commands.has_permissions( administrator = True)
async def _prefix(ctx, arg: str = None):
    if arg is None:
        emb = discord.Embed(title = "✅ | Изменение префикса", description = "Введите префикс, на какой хотите поменять?", colour = discord.Color.red())
        emb.add_field(name = "Пример использования комманды", value = f"{ctx.prefix}prefix <ваш префикс>")
        await ctx.send(embed = emb)
    elif len(str(arg)) > 5:
        emb = discord.Embed(title = "✅ | Изменение префикса", description = "Введите префикс не больше 5-ти символов", colour = discord.Color.red())
        emb.add_field(name = "Пример использования комманды", value = f"{ctx.prefix}prefix <ваш префикс>")
        await ctx.send(embed = emb)
    else:
        collection.update_one({"guild_id": ctx.guild.id}, {"$set": {"prefix": arg}})
        
        emb = discord.Embed(title = "✅ | Изменение префикса", description = f"Префикс сервера был обновлён на: {arg}", colour = discord.Color.green())
        await ctx.send(embed = emb)

@_prefix.error
async def _prefix_error(ctx, error ):
    if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)

#TWITCH
@client.event
async def on_member_update(before, after):
    if not before.activity.type == after.activity.type:
        return

    channel = get(after.guild.channels, id= 690922480734437439)

    if isinstance(after.activity, Streaming):
        await channel.send(f"{before.mention} начал стримить на {activity.platform}: {activity.name}.\nСсылка: {activity.url}")
    elif isinstance(before.activity, Streaming):
        await channel.send(f'{after.mention} закончил стрим, как печально!')
    else:
        return            

client.run(os.environ["BOT_TOKEN"])

'''
# Это для теста
client.run('1zQ0NTcwMTYxMjAxNDE0MTU2.XzlI_w.UYJ_9BnnTjo9IFDr6_eylyjesmg')
'''