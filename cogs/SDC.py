import discord
from discord.ext import commands
from discord.utils import get

from module.catdivamodule import api
import requests

SDC = api.SDC

class SDC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = ['SDC', True]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[Monitoring]SDC был загружен[]')

        url = 'https://api.server-discord.com/v2/bots/:id/stats'
        pathparameters = {'id': '737324393117778020'}
        headers = {'Authorization': SDC}

        response = requests.post(url, pathparameters, headers=headers)


def setup(client):
    client.add_cog(SDC(client))
