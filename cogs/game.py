import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot 

import json
import random
import asyncio
import requests
import datetime

class game(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cog_name = ["игры"]
#
#Все игры были спизжены
#https://github.com/AlekseyZz/Flags-mini-game-discord.py-
#https://github.com/LEv145/AmITegoDevBot/blob/master/Modules/fun.py
#
    @commands.Cog.listener()
    async def on_ready(self):
        print('[]игры был запущин[]')

    @commands.command(
        aliases=['монетка', 'орел_решка','о_р','орёл_решка'],
        description='Бот подбрасывает монетку',
        usage='монетка'
    )
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
                                   

    @commands.command(
        aliases=["кнб", "камень_ножницы_бумага"],
        description='Игра в камень-ножницы-бумага',
        usage='кнб <камень/ножницы/бумага>'
    )
    async def rsp(self, ctx, mess):
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

    @commands.command(
        aliases=["флаги", "flags"],
        description="Сыграть в угадывания флагов стран",
        usage="флаги"
    ) # создаём команду
    async def _флаги(self, ctx): # функцию
        event_members = {} # создаём словарь, он нужен для того, чтобы подсчитывать баллы каждого участника игры
        with open('./Data/DataBase/flags.json','r',encoding='utf8') as f: # открываем файл с кодировкой utf8, чтобы всё было ок
            flags = json.load(f) # превращаем в словарь
            count = 1 # подсчёт раундов
            flags_list = [] # создаётся список, в который будут добавляться названия флагов, для того чтобы потом при помощи проверки не допускать повторов в игре
            while count <= 10:# всего 10 раундов, Вы можете изменить это значение
                otvet = random.choice(flags['Флаги']) # выбираем рандомный флаг, который скинет бот и будет ожидать ответа к нему (всё из файла flags.json)
                if otvet in flags_list: # проверка, был ли этот флаг уже в списке или нет
                    pass
                elif otvet not in flags_list: # проверка, срабатывающая, когда флага в списке нет
                    flags_list.append(otvet) # добавляет флаг в список, чтобы потом при проверке избежать повторов
                    e = discord.Embed(title = f"Флаг {count}") # создаём эмбед, с названием "Флаг №", на месте номера будет число раунда
                    e.set_image(url = otvet['url']) # ставит изображение, взяв ссылку из файла flags.json
                    await ctx.send(embed = e) # отправляет эмбед
                    def check(m):
                        return m.content.lower() == otvet['answer'].lower() and m.channel == ctx.channel

                    msg = await self.client.wait_for('message', check=check) # ожидает ответа
                    if str(msg.author.id) not in event_members: # проверка на то, есть ли автор ответа в нашем созданном ранее словаре, если нет то заносит и даёт количество очков 1
                        event_members[str(msg.author.id)] = {} # заносим в словарь
                        event_members[str(msg.author.id)]["score"] = 1 # количество очков задаём
                    elif str(msg.author.id) in event_members: # если автор ответа уже есть в ранее созданном словаре - срабатывает эта проверка
                        event_members[str(msg.author.id)]["score"] += 1 # добавляет 1 очко
                    em = discord.Embed(title = "Правильный ответ!") # создаём эмбед, который говорит о том что был правильный ответ
                    em.add_field(name = "Ответил:", value = f"{msg.author.mention}") # кто ответил
                    em.add_field(name = "Правильный ответ:",value = f"{otvet['answer']}") # какой правильный ответ
                    await ctx.channel.send(embed = em) # отправляет
                    count = count + 1 # следующий раунд
                    await asyncio.sleep(1) # ждём, чтобы всё слишком быстро не было
                    if count == 11: # если так называемый 11 раунд (конец по умолчанию) то эта проверка срабатывает
                        e = discord.Embed(title = "Конец игры!", description = f"Таблица лидеров:") # создаёт эмбед с таблицой участников, и их баллами
                        leaders = sorted(event_members, key=lambda score: event_members[score]['score'], reverse=True) # сортирует словарь по ключу score (очки)
                        position = 1 # начинаем с 1 чела в таблице
                        for leader in leaders: # создаём цикл для перебора словаря
                            leader = self.client.get_user(int(leaders[position-1])) # получаем человека
                            leader_score = event_members[str(leader.id)]['score'] # получаем очки этого человека
                            e.add_field(name=f"{position} место:", value=f"{leader.mention} | очки: **{leader_score}**",inline=False) # заносим в его нашу таблицу
                            position += 1 # строчка, чтобы далее перебирать всех
                        await ctx.send(embed = e) # отправляет эмбед объявляя конец
                        return # конец, ценок!       

def setup(client):
    client.add_cog(game(client))