import discord
from discord.ext import commands
from discord.utils import get

import requests
from module.catdivamodule import api

BOTI = api.BotiCord

class BotiCord(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cog_name = ['BotiCord', True]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[Monitoring]BotiCord был загружен[]')

        url = 'https://boticord.top/api/stats'
        headers = {'Authorization': BOTI}
        data = {
            "server": len(self.client.guilds)
        }

        response = requests.post(url, headers=headers, json=data)


def setup(client):
    client.add_cog(BotiCord(client))