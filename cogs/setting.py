import discord
from discord.ext import commands
from discord.utils import get

#from module.catdivamodule import reportDB
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://senpai:HkDTEJPgO0j51s3q@cluster0.9oqq5.mongodb.net/catdivadb?retryWrites=true&w=majority")
collection = cluster.catdivadb.settingreport

class setting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["настройки", True]


    @commands.command(aliases=['report-channel', 'reports-channel', 'reports_channel', 'канал-жалоб'])
    @commands.has_permissions(administrator=True)
    async def report_channel(self, ctx, on_off=None, channel: discord.TextChannel=None):
        if on_off is None:
            embed = discord.Embed(title="Ошибка", description="Укажите включение/выключение системы жалоб `>report-channel <on/off> <channel>`", color=discord.Color.red())
            await ctx.send(embed=embed)
        elif on_off == 'off':
            if not collection.find_one({"guild_id": ctx.guild.id}):
                embed = discord.Embed(title="Ошибка", description=f"Невозможно отключить систему жалоб!\nСистема жалоб не включена", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Система Жалоб", description=f"Система для жалоб успешно выключена на данном сервере!", color=discord.Color.green())
                await ctx.send(embed=embed)
                collection.delete_one({"guild_id": ctx.guild.id})
        elif on_off == 'on':
            if channel is None:
                embed = discord.Embed(title="Ошибка", description="Укажите канал для жалоб `>report-channel <on/off> <channel>`", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                if not collection.find_one({"guild_id": ctx.guild.id}):
                    embed = discord.Embed(title="Канал Жалоб", description=f"Канал для жалоб успешно задан - {channel.mention}", color=discord.Color.green())
                    await ctx.send(embed=embed)
                    collection.insert_one({"guild_id": ctx.guild.id, "channel_id": channel.id})
                else:
                    collection.delete_one({"guild_id": ctx.guild.id})
                    collection.insert_one({"guild_id": ctx.guild.id, "channel_id": channel.id})
                    embed = discord.Embed(title="Канал Жалоб", description=f"Канал для жалоб успешно задан - {channel.mention}", color=discord.Color.green())
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Ошибка", description="Укажите включение/выключение системы жалоб `>report-channel <on/off> <channel>`", color=discord.Color.red())
            await ctx.send(embed=embed)    
        
def setup(client):
    client.add_cog(setting(client))   

''' 
**Правила поведения на сервере**: 
1. Уважайте других участников сервера 
1.1. Не оскорбляйте других. 
1.2. Не пишите капсом (ВОТ ТАК БОЛЬШИМИ БУКВАМИ). 
1.3. Не используйте чрезмерное количество мата, эмодзи и повторяющихся сообщений. 
1.4. Нельзя вести дискуссии на политические и религиозные темы. 
1.5. Нельзя провоцировать на конфликт. 
1.6. Запрещен флуд в любом его проявлении (Огромное количество смайлов, стикеров, необоснованно большое количество сообщений подряд) 
1.7. Запрещено бесконечное нытье на какие-либо темы. 
1.8. Запрещены спойлеры к играм/фильмам/сериалам и т.д.
1.9. Запрещено использовать аватар, писать сообщения, размещать картинки, несущие порнографический характер или разжигающий межнациональные конфликты.
1.10. Запрещенно выпрашивать оценку канала и тд. 

Нарушение этих правил карается  МУТом  на сутки (или более) на текстовых и  голосовых каналах, а то и БАНом.

2. Реклама на сервере.
2.1. Запрещено размещать ссылки на чужие дискорд сервера в текстовых чатах.(в том числе и в лс) 
2.2. Запрещено покупать и продавать ключи от игр и скины.
2.3. Запрещена любая рекламная деятельность.

**Администрация сервера оставляет последнее слово за собой.**

**Не прикрывайтесь недочетами правил, этот список всегда можно дополнить. Если модератор вас о чем-то просит, значит в этом есть необходимость**  	
'''
