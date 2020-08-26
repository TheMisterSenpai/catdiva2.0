import discord
from discord.ext import commands
from discord.utils import get

class event(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Зачем ты зашел в этот файл, он так для красоты
    @commands.command
    async def on_member_update(self, before, after):
        if before.nick != after.nick:#проверка на смену ника
            channel = client.get_channel(727184938050256906)#ид канала куда будет отправляться сообщение
            emb = discord.Embed(title = '', description = f'**Пользователь {before.mention} сменил ник.**', colour = discord.Color.red())
            emb.add_field(name = '**Старый ник**', value = f'{before.nick}') 
            emb.add_field(name = '**Новый ник**', value = f'{after.nick}') 
            emb.set_footer(text = 'Спасибо за использования нашего бота')

            await channel.send(embed = emb)


    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен event.py')    

def setup(client):
    client.add_cog(event(client))                