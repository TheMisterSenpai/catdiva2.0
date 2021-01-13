import discord
from discord.ext import commands
from discord.utils import get

from module.catdivamodule import api
from pymongo import MongoClient

MONGO = api.MONGO

cluster = MongoClient(MONGO)
collection = cluster.catdivadb.settingreport

class reportsetting(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["канал-жалоб настройки", True]

    @commands.Cog.listener()
    async def on_ready(self):
        print('[]канал-жалоб настройки был включен[]')


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
    client.add_cog(reportsetting(client))   