import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot 

import json
import random
import asyncio
import requests

class game(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["Игры", True]
#Код https://github.com/AlekseyZz/Flags-mini-game-discord.py-
    
	@commands.command(aliases=['лотерея', 'рандомный_человек', 'rand_membed'], description="Лотерея на всём сервере",
                      usage="лотерея <None>")
    async def lottery(self, ctx):
        member = random.choice(ctx.guild.members)
        await ctx.send(f"{member.display_name} - счастливчик")
                                   
    @commands.command(aliases=["монетка" 'орел_решка','о_р','орёл_решка'],description='Бот подбрасывает монетку',usage='монетка <None>')
    async def o_r(self, ctx):
        robot = ["орёл", "решка"]
        robot_choice = random.choice(robot)
                                   
        emb = discord.Embed(title="Орел или решка", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
        emb.set_author(name="⠀", icon_url="https://www.iconpacks.net/icons/2/free-dollar-coin-icon-2139-thumb.png")
        emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
                                   
        if robot_choice == "орёл":
            emb.add_field(name="Подбрасываем монетку....", value="**Орёл**")

        if robot_choice == "решка":
            emb.add_field(name="Подбрасываем монетку....", value="**Решка**")

        await ctx.send(embed=emb)
                                   

    @commands.command(aliases=["кнб", "камень_ножницы_бумага"],description='Игра в камень-ножницы-бумага',usage='кнб <камень/ножницы/бумага>')
    async def rsp(self,ctx, mess):
        robot = ['Камень', 'Ножницы', 'Бумага']
        stone_list = ["stone", "камень","к"]
        paper_list = ["paper", "бумага", "б"]
        scissors_list = ["scissors", "ножницы","н"]  
                                   
        out = {"icon": None, "value": None, "img": None}
                                   
        robot_choice = random.choice(robot)  
                                   
        win_list = ["Вы выиграли!","Вы проиграли :с", "Ничья!"]
            
        # Embed
        emb = discord.Embed(title=robot_choice, colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                                   
        if mess.lower() in stone_list:       
            if robot_choice == 'Ножницы':
                win = win_list[0]
                out["icon"] = "✂"
            elif robot_choice == 'Бумага':
                win = win_list[1]
                out["icon"] = "🧻"
            else:
                win = win_list[2]
                out["icon"] = "🥔"

        elif mess.lower() in paper_list:
            if robot_choice == 'Камень':
                win = win_list[0]
                out["icon"] = "🥔"     
            elif robot_choice == 'Ножницы':
                win = win_list[1]
                out["icon"] = "✂"             
            else:
                win = win_list[2]
                out["icon"] = "🧻"               

        elif mess.lower() in scissors_list:
            if robot_choice == 'Бумага':
                win = win_list[0]
                out["icon"] = "🧻"               
            elif robot_choice == 'Камень':
                win = win_list[1]
                out["icon"] = "🥔"                
            else:
                win = win_list[2]  
                out["icon"] = "✂"     
        else:
            await ctx.send("Ошибка!")
            return
                
        if win == "Вы выиграли!":
            out["img"] = "https://im0-tub-ru.yandex.net/i?id=12af96d2422023b2e8c0854c6960d229&n=13&exp=1"
        elif win == "Вы проиграли :с":
            out["img"] = "https://thumbs.dreamstime.com/b/%D0%BF%D0%BE%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-87995106.jpg"
        else:
            out["img"] = "https://avatanplus.com/files/resources/original/574454ca56620154e2eb3672.png"
                                   
        emb.add_field(name=out["icon"], value=win)
        emb.set_author(name="⠀",
        icon_url=out["img"])
        emb.set_footer(icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(game(client))