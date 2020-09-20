import discord
from discord.ext import commands
from discord.utils import get

bad_words = [ 'cука', 'педик', 'пидор', 'гандон', 'блять', 'пидорас', 'уёбок', 'уебок', 'даун', 'еблан' ]

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message ( message ):
	    await client.process_commands( message )

	    msg = message.content.lower()

	    if msg in bad_words:
		    await message.delete()
		    await message.author.send(f'{message.author.name} не пиши в чат такие слова ')      

def setup(client):
    client.add_cog(moderation(client)) 