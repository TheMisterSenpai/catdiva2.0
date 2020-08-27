import ast
import discord
import config
from Utils import DB
from discord.ext import commands

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.cog_name = ["Специальное"]

    # Да, Да, я спиздил код с гитхаба кое-какого, давайте, убейте меня.
    @commands.command(
        aliases=["eval"],
        description="Выполнение кода",
        usage="eval <код>")
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        try:
            fn_name = "_eval_expr"

            cmd = cmd.strip("` ")

            # add a layer of indentation
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

            # wrap in async def body
            body = f"async def {fn_name}():\n{cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))
            await ctx.send(result)

        except Exception as error:
            return await ctx.send(embed=discord.Embed(description=f'❗️ {ctx.author.name}, В вашем коде произошла следующая ошибка:\n`{error}`', color=config.COLOR_ERROR))

    @commands.command(
        aliases=["set_private"],
        description="Настройка Приваток Бота",
        usage="set_private <None>")
    @commands.has_permissions(administrator=True)
    async def setprivate(self, ctx):
        await ctx.send("Введите ID Категории для приватных каналов (у вас 60 секунд)")
        category = await self.bot.wait_for('message', timeout=60.0, check=lambda
            message: message.author == ctx.author and message.channel == ctx.channel)

        await ctx.send("Введите ID Канала для создания приватных каналов (у вас 60 секунд)")
        channel = await self.bot.wait_for('message', timeout=60.0, check=lambda
            message: message.author == ctx.author and message.channel == ctx.channel)

        data = [
            {"name": "channels", "update": f"private = '{channel.content}'", "insert": f'{channel.content}, null'},
            {"name": "category", "update": f"private = '{category.content}'", "insert": f'{category.content}'}
        ]
        DB.Set().options(data)
        await ctx.send("Настройки успешно сохранены!")

def setup(client):
    client.add_cog(special(client))        