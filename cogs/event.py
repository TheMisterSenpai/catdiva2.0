import discord
from discord.ext import commands
from discord.utils import get

import config

class event(commands.Cog):

    def __init__(self, bot):
        self.bot= bot
        self._last_member = None
        self.cog_name = ["Ивенты", True]
    #Зачем ты зашел в этот файл, он так для красоты

              
def setup(client):
    client.add_cog(event(client))                