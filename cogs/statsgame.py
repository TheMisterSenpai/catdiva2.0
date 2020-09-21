import discord
from discord.ext import commands
from discord.utils import get

import socket
from mcstatus import MinecraftServer

class statsgame(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Статистика игр"]

    @commands.command(
        aliases=["майн", "мс", "minecraft", "mine"],
        usage="mc <ip> [port]",
        description="Информация о Minecraft сервере")
    async def _mc(self, ctx, ip, port=None):
        message = await ctx.send("Идёт сбор информации, пожалуйста подождите.")
 
        if port is None:
            server = MinecraftServer.lookup(f"{ip}:25565")
        else:
            try:
                server = MinecraftServer.lookup(f"{ip}:{port}")
            except ValueError:
                embed = discord.Embed(title="Ошибка Подключения", description="Порт вне допустимого диапазона **0-65535**.",
                                      color=0xb20000)
                await message.delete()
                return await ctx.send(embed=embed)
 
        try:
            server_ping = server.ping()
            server_status = server.status()
 
        except socket.timeout:
            players = "`❌ Не Доступно`"
            version = "`❌ Не Доступно`"
            description = "`❌ Не Доступно`"
            ping = "`❌ Не Доступно`"
            status = "🔴 Отключен"
 
        except socket.gaierror:
            embed = discord.Embed(title="Ошибка Ввода", description="Вы ввели не действительный IP или Порт.", color=0xb20000)
            await message.delete()
            return await ctx.send(embed=embed)
 
        except IOError as error:
            embed = discord.Embed(title="Ошибка Подключение", description="Мне не удалось получить информацию с этого сервера.\n"
                                                                          "Возможно у него стоит какая-та защита.\n\n"
                                                                          f"`Ошибка: {error}`",
                                  color=0xb20000)
            await message.delete()
            return await ctx.send(embed=embed)
 
        else:
            players = f"{server_status.players.online}/{server_status.players.max}"
            version = server_status.version.name
 
            if 'extra' in server_status.description:
                description = f"\n- {server_status.description['extra'][0]['text']}\n" \
                              f"- {server_status.description['extra'][1]['text']}\n" \
                              f"- {server_status.description['extra'][2]['text']}"
            else:
                description = server_status.description['text']
 
            ping = server_ping
            status = "🟢 Включен"
 
        if status == "🟢 Включен":
            try:
                server_query = server.query()
 
            except socket.timeout:
                query = "Query отключен на сервере"
 
            else:
                query = f"**Хост:** {server_query.host}\n" \
                        f"**Софт:** {server_query.software}\n" \
                        f"**MOTD:** {server_query.motd}\n" \
                        f"**Плагины:** {''.join(server_query.plugins)}\n" \
                        f"**Игроки:** {', '.join(server_query.players.names)}"
 
        else:
            query = "`❌ Не Доступно`"
 
        embed = discord.Embed(
            title="Статус Travedit Сервер",
            description=f"**IP:** {ip}\n"
                        f"**Описание:** {description}\n"
                        f"**Версия:** {version}",
            color=0xFF7F3F)
        embed.add_field(name="Игроки", value=players, inline=False)
        embed.add_field(name="Статус", value=status, inline=False)
        embed.add_field(name="Пинг", value=ping, inline=False)
        embed.add_field(name="Данные через Query",
                        value=query,
                        inline=False)
 
        await message.edit(content=None, embed=embed)

def setup(client):
    client.add_cog(statsgame(client)) 