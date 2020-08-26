import discord
import os
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
import json

client = commands.Bot( command_prefix = '.' )
#Role auto
@client.event

async def on_member_join( member ):
	channel = client.get_channel( 690922367186239498 )#Исправил

	role = discord.utils.get( member.guild.roles, id = 690915819340824579 )

	await member.add_roles( role )
#
#cogs
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="Сервер C:", url='https://www.twitch.tv/themistersenpai')) 

@client.command()
async def load(ctx, extensions):
    client.load_extension(f'cogs.{extensions}')


@client.command()
async def reload(ctx, extensions):
    client.unload_extension(f'cogs.{extensions}')
    client.load_extension(f'cogs.{extensions}')


@client.command()
async def unload(ctx, extensions):
    client.unload_extension(f'cogs.{extensions}')


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
    channel = client.get_channel(721412116573323298)    
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
#lvl
@client.event
async def on_message( message ):
	await client.process_commands( message )

	if not message.author.bot:
		with open('lvl.json',"r") as f:
			users = json.load(f)

		channel_log = client.get_channel( 690922597805719613 ) # ID - канала, в который будет отправлятся уведомление о повышении
		async def update_ranked(users, user):
			if not user in users:
				users[user] = {}
				users[user]['exp'] = 0
				users[user]['lvl'] = 1
		async def add_exp(users, user, exp):
			users[user]['exp'] += exp
		async def add_lvl(users, user):
			exp = users[user]['exp']
			lvl = users[user]['lvl']
			if exp > lvl:
				await channel_log.send(f'**{message.author.mention}** повысил свой уровень до {lvl}!')
				users[user]['exp'] = 0
				users[user]['lvl'] = lvl + 1
		async def add_rank(users, user):
			lvl = users[user]['lvl']
			rank10 = discord.utils.get( message.guild.roles, id = 693003614431739965 ) # id Роли
			rank25 = discord.utils.get( message.guild.roles, id = 693003740902326272 )
			rank30 = discord.utils.get( message.guild.roles, id = 693003820141379606 )
			rank50 = discord.utils.get( message.guild.roles, id = 693004374691020872 )
			rank1000 = discord.utils.get( message.guild.roles, id = 6693004942864023625 )
			
			if lvl == 10:
				await channel_log.send(f"**{message.author.mention}** получил новый ранг {rank10}!")
				await message.author.add_roles(rank10, reason=None, atomic=True)
				users[user]['lvl'] = lvl + 1

			if lvl == 25:
				await channel_log.send(f'**{message.author.mention}** получил новый ранг {rank25}')
				await message.author.add_roles(rank20, reason=None, atomic=True)
				users[user]['lvl'] = lvl + 1
				# Это удаляет роль после получения новой
				await message.author.remove_roles(rank10)
			
			if lvl == 30:
				await channel_log.send(f'**{message.author.mention}** получил новый ранг {rank30}')
				await message.author.add_roles(rank20, reason=None, atomic=True)
				users[user]['lvl'] = lvl + 1
				# Это удаляет роль после получения новой
				await message.author.remove_roles(rank25)
			
			if lvl == 50:
				await channel_log.send(f'**{message.author.mention}** получил новый ранг {rank50}')
				await message.author.add_roles(rank20, reason=None, atomic=True)
				users[user]['lvl'] = lvl + 1
				# Это удаляет роль после получения новой
				await message.author.remove_roles(rank30)

			if lvl == 1000:
				await channel_log.send(f'**{message.author.mention}** получил новый ранг {rank50}')
				await message.author.add_roles(rank20, reason=None, atomic=True)
				users[user]['lvl'] = lvl + 1
							
		await update_ranked(users,str(message.author.id))
		
		await add_exp(users,str(message.author.id),0.2) # 1 - сколько опыта получает пользователь за 1 сообщение
		await add_lvl(users,str(message.author.id))
		await add_rank(users,str(message.author.id))
		with open('lvl.json',"w") as f:
			json.dump(users,f)
#
#
@client.event
async def on_member_update(self, before, after):
    if before.nick != after.nick:#проверка на смену ника
        channel = client.get_channel(727184938050256906)#ид канала куда будет отправляться сообщение
        emb = discord.Embed(title = '', description = f'**Пользователь {before.mention} сменил ник.**', colour = discord.Color.red())
        emb.add_field(name = '**Старый ник**', value = f'{before.nick}') 
        emb.add_field(name = '**Новый ник**', value = f'{after.nick}') 
        emb.set_footer(text = 'Спасибо за использования нашего бота')

        await channel.send(embed = emb)
#

client.run('NzQ0NTcwMTYxMjAxNDE0MTU2.XzlI_w.Ig0plFkOY1gESkc_qQ7fabNiJHs')        