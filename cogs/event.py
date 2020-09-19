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

    @commands.Cog.listener() 
    async def on_member_message(self, member):
        await client.process_commands( message )

	    if not message.author.bot:
		    with open('./Data/DataBase/economy.json',"r") as f:
			    users = json.load(f)

        async def update_money(users, user):
            if not user in users:
                users[user] = {}
                users[user]['money'] = 300    

		with open('./Data/DataBase/economy.json',"w") as f:
			json.dump(users,f)            
   
def setup(client):
    client.add_cog(event(client))                