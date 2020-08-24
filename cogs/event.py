import discord
from discord.ext import commands
from discord.utils import get

class event(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Зачем ты зашел в этот файл, он так для красоты
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен event.py')    

def setup(client):
    client.add_cog(event(client))                