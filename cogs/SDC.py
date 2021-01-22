import discord
from discord.ext import commands
from discord.utils import get

from module.catdivamodule import api
import requests
import json

SDC = api.SDC

class SDC(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = ['SDC', True]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[Monitoring]SDC был загружен[]')

        url =f'https://api.server-discord.com/v2/bots/737324393117778020/stats'
        headers = {'Authorization': SDC}
        data: dict = {
            'server_count': len(self.client.guilds)
        }

        response = requests.post(url, headers=headers, data=data)


def setup(client):
    client.add_cog(SDC(client))
