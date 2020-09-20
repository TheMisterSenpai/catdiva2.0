import discord
from discord.ext import commands
from discord.utils import get

import json

class achievements(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Достижения", True]

#СКОРО

def setup(client):
    client.add_cog(achievements(client))