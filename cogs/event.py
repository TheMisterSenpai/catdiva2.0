import discord
from discord.ext import commands
from discord.utils import get

import config
from Utils import DB

class event(commands.Cog):

    def __init__(self, bot):
        self.bot= bot
        self._last_member = None
        self.cog_name = ["Ивенты", True]
    #Зачем ты зашел в этот файл, он так для красоты

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        Get = DB.Get()
        Set = DB.Set()
        if after.channel:
            channel = Get.options("channels")[0]
            category = Get.options("category")[0]

            if int(after.channel.id) == int(channel):
                cat = discord.utils.get(member.guild.categories, id=int(category))
                channel2 = await member.guild.create_voice_channel(name=f"{member.name}#{member.discriminator}",
                                                                   category=cat)
                await member.move_to(channel2)
                await channel2.set_permissions(member, manage_channels=True)
                Set.privateChannels(channel2, member)

            elif before.channel:
                if str(before.channel.id) in str(Get.privateChannels(member)[0]):
                    try:
                        await before.channel.delete()
                    except Exception:
                        pass

        else:
            if before.channel:
                if str(before.channel.id) in str(Get.privateChannels(member)[0]):
                    try:
                        await before.channel.delete()
                    except Exception:
                        pass


    @commands.Cog.listener() #Дает 0 варнов кто присоединился
    async def on_member_join(self, member):
        
        conn = sqlite3.connect('./Data/DataBase/warn_users.db')
        cursor = conn.cursor()

        if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
            cursor.execute(f"INSERT INTO users VALUES('{member.id}', 0)")
            conn.commit()
        else:
            pass

    @commands.Cog.listener() #Убирает человека который вышел с сервера
    async def on_member_remove(self, member):

        conn = sqlite3.connect('./Data/DataBase/warn_users.db')
        cursor = conn.cursor()

        if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
            cursor.execute(f"DELETE FROM users WHERE id = {member.id}")
            conn.commit()
        else:
            pass    
                  
   
def setup(client):
    client.add_cog(event(client))                