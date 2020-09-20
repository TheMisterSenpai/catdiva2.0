import discord
from discord.ext import commands
from discord.utils import get
from config import PREFIX

class command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._last_member = None
        self.cog_name = ["команды"]

    @commands.command(
        aliases=["хелп", "команды", "comms", "commands", "помощь"],
        description="Это сообщение",
        usage="help [модуль]")
    async def help(self, ctx, name=None):
        if name is not None:
            name = name.lower()
 
        prefix = config.prefix # беру данные из конфига. Подстраивайте под себя
        color = config.color # цвет ембеда
 
        copy_text = config.text # для футера
        copy_icon = config.icon # для футера
 
        cogs = []
        for i in self.client.cogs: # у меня переменная bot. Тоже подстраивайте под себя
            cog = self.client.cogs[i]
            hide = len(cog.cog_name)
            if hide == 1:
                cogs.append(f"{cog.cog_name[0].lower()}")
 
        if not name:
            embed = discord.Embed(
                description=f"{ctx.author.display_name}, Чтоб узнать список команд пропишите **{prefix}help "
                            f"<модуль>**\n"
                            f"**Доступные модули:** {', '.join(cogs)}", color=color)
            await ctx.send(embed=embed)
        else:
            if name in cogs:
                cog = None
                namec = None
                for i in self.client.cogs:
                    coge = self.client.cogs[i]
                    if name in coge.cog_name[0].lower():
                        cog = coge
                        namec = i
                        break
 
                name = cog.cog_name[0]
                comm_list = []
 
                for command in self.client.commands:
                    if command.cog_name == namec:
                        if not command.hidden:
                            comm_list.append(
                                f"**{command.aliases[0]}:** {command.description}\n`{prefix}{command.usage}`\n\n")
 
                embed = discord.Embed(
                    title=f"Help | {name}",
                    description=f"".join(comm_list),
                    color=color)
                embed.set_footer(text=copy_text, icon_url=copy_icon)
                embed.set_thumbnail(
                    url='https://pngimg.com/uploads/question_mark/question_mark_PNG93.png')
 
                await ctx.send(embed=embed)
 
            else:
                embed = discord.Embed(
                    description=f"{ctx.author.display_name}, Модуль не найден!\nЧтоб узнать список команд пропишите "
                                f"{prefix}help <модуль>\n"
                                f"**Доступные модули:** {', '.join(cogs)}")
                await ctx.send(embed=embed)



def setup(client):
    client.add_cog(command(client)) 