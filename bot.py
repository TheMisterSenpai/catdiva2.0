import discord
import os
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

import json
from module.catdivamodule import config
import nest_asyncio

from module.catdivamodule.loops import Loop
from colorama import Fore, Style
from colorama import init 


PREFIX = config.PREFIX
STATUS = config.STATUS
STATUSURL = config.STATUSURL
COLOR_ERROR = config.COLOR_ERROR

client = commands.Bot( command_prefix =  PREFIX )
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
#

#Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Команда не найдена!', color=COLOR_ERROR))
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, У бота недостаточно прав!\n'
                                                              f'❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций.', color=color))
    elif isinstance(error, commands.MissingPermissions) or isinstance(error, discord.Forbidden):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, У вас недостаточно прав!', color=COLOR_ERROR))
    elif isinstance(error, commands.BadArgument):
        if "Member" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Пользователь не найден!', color=COLOR_ERROR))
        if "Guild" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Сервер не найден!', color=COLOR_ERROR))
        else:
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Введён неверный аргумент!', color=COLOR_ERROR))
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Пропущен аргумент с названием {error.param.name}!', color=COLOR_ERROR))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Воу, Воу, Не надо так быстро прописывать команды.\n'
                                                       f'❗️ Подожди {error.retry_after:.2f} секунд и сможешь написать команду ещё раз.'))
    else:
        if "ValueError: invalid literal for int()" in str(error):
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, Укажите число а не строку!', color=COLOR_ERROR))
        else:
            print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Команда: {ctx.message.content}")
            print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Сервер:  {ctx.message.guild}")
            print(Fore.RED + f"[ERROR] " + Style.RESET_ALL + f"Ошибка:  {error}")
            await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, \n**`ERROR:`** {error}', color=COLOR_ERROR))
            raise error

#

#Role auto
@client.event
async def on_member_join( member ):
	channel = client.get_channel( 690922367186239498 )#Исправил

	role = discord.utils.get( member.guild.roles, id = 761927608442552320 )

	#role = discord.utils.get( member.guild.roles, id = 751468991075319903 )

	#role = discord.utils.get( member.guild.roles, id = 751468342916677694 )

	await member.add_roles( role )  
#
#cogs
@client.command()
async def load(ctx, extensions):
    if ctx.author.id == 364437278728388611:
        client.load_extension(f'cogs.{extensions}')
    else:
        await ctx.send(f'Вы не создатель {ctx.author}')

@client.command()
async def reload(ctx, extensions):
    if ctx.author.id == 364437278728388611:
        client.unload_extension(f'cogs.{extensions}')
        client.load_extension(f'cogs.{extensions}')
    else:
        await ctx.send(f'Вы не создатель {ctx.author}')

@client.command()
async def unload(ctx, extensions):
    if ctx.author.id == 364437278728388611:
        client.unload_extension(f'cogs.{extensions}')
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
#
#report
@client.command()
async def report(ctx, member:discord.Member=None, *, arg=None):
    message = ctx.message
    channel = client.get_channel(749869445224202350)    
    if member == None:
        await ctx.send(embed=discord.Embed(description='Укажите пользователя!', color=discord.Color.red()))
    elif arg == None:
        await ctx.send(embed=discord.Embed(description='Укажите причину жалобы!', color=discord.Color.red()))
    else:
        emb = discord.Embed(title=f'Жалоба на пользователя {member}', color=discord.Color.blue())
        emb.add_field(name='Автор жалобы:', value=f'*{ctx.author}*')
        emb.add_field(name='Причина:', value='*' +arg + '*')
        emb.add_field(name='ID жалобы:', value=f'{message.id}')
        await channel.send(embed=emb)
        await ctx.author.send('✅ Ваша жалоба успешно отправлена!')       
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

client.run(os.environ["BOT_TOKEN"])   

''' Это для теста
client.run('') 
'''