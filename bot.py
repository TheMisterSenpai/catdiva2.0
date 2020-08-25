import discord
import os
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks

client = commands.Bot( command_prefix = '.' )

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

client.run('NzQ0NTcwMTYxMjAxNDE0MTU2.XzlI_w.Ig0plFkOY1gESkc_qQ7fabNiJHs')        