import datetime
import discord
from discord.ext import commands
import json

class Suggest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA
        self.considered = 0xffd500
        self.approved = 0x66FF66
        self.implemented = 0x6633ff

    @commands.command()
    @commands.cooldown(rate = 1, per = 300, type = commands.BucketType.member)
    async def suggest(self, ctx, *, suggestion = None):
        """
        Create a suggestion.
        """
        if suggestion == None:
            embed = discord.Embed(
                title = "Ошибка Предложения",
                description = "Пожалуйста, предоставьте предложение!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            suggest.reset_cooldown(ctx)
        else:
            with open(r"./Data/DataBase/suggestion_channels.json", "r") as f:
                suggestion_channels = json.load(f)
            with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
                suggestion_log_channels = json.load(f)
            with open(r"./Data/DataBase/staff_roles.json", "r") as f:
                staff_roles = json.load(f)
            with open(r"./Data/DataBase/suggestions.json", "r") as f:
                suggestions = json.load(f)
            with open(r"./Data/DataBase/results.json", "r") as f:
                results = json.load(f)
            with open(r"./Data/DataBase/suggestors.json", "r") as f:
                suggesters = json.load(f)
            if str(ctx.message.guild.id) not in suggestion_channels:
                embed = discord.Embed(
                    title = "Ошибка Предложения",
                    description = "Не поставлен канал отправки предложения!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                suggest.reset_cooldown(ctx)
            else:
                suggestion_channel = suggestion_channels[str(ctx.message.guild.id)]
                embed = discord.Embed(
                    title = "Предложение поступило!",
                    color = self.blurple
                )
                suggestion_channel = discord.utils.get(ctx.guild.text_channels, id = suggestion_channel)
                msg = await suggestion_channel.send(embed = embed)
                suggestions[str(msg.id)] = suggestion
                results[str(msg.id)] = "pending"
                suggesters[str(msg.id)] = ctx.message.author.id
                with open(r"./Data/DataBase/suggestors.json", "w") as f:
                    json.dump(suggesters, f, indent = 4)
                with open(r"./Data/DataBase/suggestions.json", "w") as f:
                    json.dump(suggestions, f, indent = 4)
                with open(r"./Data/DataBase/results.json", "w") as f:
                    json.dump(results, f, indent = 4)
                embed = discord.Embed(
                    description = f"**Советчик**\n{ctx.message.author.mention}\n\n**Предложение**\n{suggestion}",
                    timestamp = datetime.datetime.utcnow(),
                    color = self.blurple
                )
                embed.set_footer(text = f"ID Предложения {msg.id}")
                await msg.edit(embed = embed)
                await msg.add_reaction("⬆")
                await msg.add_reaction("⬇")
                if str(ctx.message.guild.id) in suggestion_log_channels:
                    suggestion_log_channel = suggestion_log_channels[str(ctx.message.guild.id)]
                    suggestion_log_channel = discord.utils.get(ctx.guild.text_channels, id = suggestion_log_channel)
                    embed = discord.Embed(
                        title = "Новое предложение",
                        description = f"**Советчик**\n{ctx.message.author.mention}\n\n**Предложение**\n{suggestion}",
                        timestamp = datetime.datetime.utcnow(),
                        color = self.blurple
                    )
                    embed.set_footer(text = f"ID Предложения {msg.id}")
                    await suggestion_log_channel.send(embed = embed)

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
            title = "Перезарядка",
            description = f"Вы можете предлагать только каждые пять минут! Попробуйте через {int(error.retry_after)}s.",
            color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    @commands.command(aliases = ["accept"])
    async def approve(self, ctx, suggestion_id : discord.Message = None, *, reason = None):
        """
        Mark a suggestion as approved.
        """
        with open(r"./Data/DataBase/suggestions.json", "r") as f:
            suggestions = json.load(f)
        with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
            suggestion_log_channels = json.load(f)
        with open(r"./Data/DataBase/staff_roles.json", "r") as f:
            staff_roles = json.load(f)
        with open(r"./Data/DataBase/results.json", "r") as f:
            results = json.load(f)
        with open(r"./Data/DataBase/reasons.json", "r") as f:
            reasons = json.load(f)
        with open(r"./Data/DataBase/suggestors.json", "r") as f:
            suggesters = json.load(f)
        with open(r"./Data/DataBase/notes.json", "r") as f:
            notes = json.load(f)
        with open(r"./Data/DataBase/noters.json", "r") as f:
            noters = json.load(f)
        with open(r"./Data/DataBase/resulters.json","r") as f:
            resulters = json.load(f)
        if str(ctx.message.guild.id) not in staff_roles:
            embed = discord.Embed(
                title = "Ошибка Одобрения",
                description = "Этот сервер не имеет роли персонала!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            staff_role_id = staff_roles[str(ctx.message.guild.id)]
            staff_role = discord.utils.get(ctx.message.author.roles, id = staff_role_id)
            if staff_role == None and ctx.message.author.guild_permissions.administrator == False:
                embed = discord.Embed(
                    title = "Ошибка Одобрения",
                    description = f"Вам не хватает следующей роли: <@{staff_role_id}>!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if suggestion_id == None:
                    embed = discord.Embed(
                        title = "Ошибка Одобрения",
                        description = "Пожалуйста напишите ID Предложения!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    suggestion_id = suggestion_id.id
                    if str(suggestion_id) not in suggestions:
                        embed = discord.Embed(
                            title = "Ошибка Одобрения",
                            description = "Это неправильный ID!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
        
                    else:
                        resulters[str(suggestion_id)] = ctx.message.author.id
                        results[str(suggestion_id)] = "approved"
                        with open(r"./Data/DataBase/resulters.json", "w") as f:
                            json.dump(resulters, f, indent = 4)
                        with open(r"./Data/DataBase/results.json", "w") as f:
                            json.dump(results, f, indent = 4)
                        suggestion = suggestions[str(suggestion_id)]
                        suggestion_msg = await ctx.fetch_message(id = suggestion_id)
                        suggester = suggesters[str(suggestion_id)]
                        if str(suggestion_id) in notes:
                            noter = noters[str(suggestion_id)]
                            note = notes[str(suggestion_id)]
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Одобрено",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.approved
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Одобрено",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.approved
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        else:
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Одобрено",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.approved
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Одобрено",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.approved
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        with open(r"./Data/DataBase/reasons.json", "w") as f:
                            json.dump(reasons, f, indent = 4)
                        if str(ctx.message.guild.id) in suggestion_log_channels:
                            suggestion_log_channel = suggestion_log_channels[str(ctx.message.guild.id)]
                            suggestion_log_channel = discord.utils.get(ctx.guild.text_channels, id = suggestion_log_channel)
                            suggestion = suggestions[str(suggestion_id)]
                            if str(suggestion_id) in notes:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Одобренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.approved
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Одобренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.approved
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                            else:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Одобренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.approved
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Одобренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.approved
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)

    @commands.command()
    async def deny(self, ctx, suggestion_id : discord.Message = None, *, reason = None):
        """
        Mark a suggestion as denied.
        """
        with open(r"./Data/DataBase/suggestions.json", "r") as f:
            suggestions = json.load(f)
        with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
            suggestion_log_channels = json.load(f)
        with open(r"./Data/DataBase/staff_roles.json", "r") as f:
            staff_roles = json.load(f)
        with open(r"./Data/DataBase/results.json", "r") as f:
            results = json.load(f)
        with open(r"./Data/DataBase/reasons.json", "r") as f:
            reasons = json.load(f)
        with open(r"./Data/DataBase/suggestors.json", "r") as f:
            suggesters = json.load(f)
        with open(r"./Data/DataBase/notes.json", "r") as f:
            notes = json.load(f)
        with open(r"./Data/DataBase/noters.json", "r") as f:
            noters = json.load(f)
        with open(r"./Data/DataBase/resulters.json","r") as f:
            resulters = json.load(f)
        if str(ctx.message.guild.id) not in staff_roles:
            embed = discord.Embed(
                title = "Ошибка Отказа",
                description = "Этот сервер не имеет роли персонала!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            staff_role_id = staff_roles[str(ctx.message.guild.id)]
            staff_role = discord.utils.get(ctx.message.author.roles, id = staff_role_id)
            if staff_role == None and ctx.message.author.guild_permissions.administrator == False:
                embed = discord.Embed(
                    title = "Ошибка Отказа",
                    description = f"Вам не хватает следующей роли: <@{staff_role_id}>!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if suggestion_id == None:
                    embed = discord.Embed(
                        title = "Ошибка Отказа",
                        description = "Пожалуйста напишите ID Предложения!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    suggestion_id = suggestion_id.id
                    if str(suggestion_id) not in suggestions:
                        embed = discord.Embed(
                            title = "Ошибка Отказа",
                            description = "Это неправильный ID!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
                    else:
                        resulters[str(suggestion_id)] = ctx.message.author.id
                        results[str(suggestion_id)] = "denied"
                        with open(r"./Data/DataBase/resulters.json", "w") as f:
                            json.dump(resulters, f, indent = 4)
                        with open(r"./Data/DataBase/results.json", "w") as f:
                            json.dump(results, f, indent = 4)
                        suggestion = suggestions[str(suggestion_id)]
                        suggestion_msg = await ctx.fetch_message(id = suggestion_id)
                        suggester = suggesters[str(suggestion_id)]
                        if str(suggestion_id) in notes:
                            noter = noters[str(suggestion_id)]
                            note = notes[str(suggestion_id)]
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Отказано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.errorcolor
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Отказано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.errorcolor
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        else:
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Отказано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.errorcolor
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Отказано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.errorcolor
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        with open(r"Data/reasons.json", "w") as f:
                            json.dump(reasons, f, indent = 4)
                        if str(ctx.message.guild.id) in suggestion_log_channels:
                            suggestion_log_channel = suggestion_log_channels[str(ctx.message.guild.id)]
                            suggestion_log_channel = discord.utils.get(ctx.guild.text_channels, id = suggestion_log_channel)
                            suggestion = suggestions[str(suggestion_id)]
                            if str(suggestion_id) in notes:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Предложение Отказано",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.errorcolor
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Предложение Отказано",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.errorcolor
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                            else:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Предложение Отказано",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.errorcolor
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Предложение Отказано",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.errorcolor
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)

    @commands.command(aliases = ["maybe"])
    async def consider(self, ctx, suggestion_id : discord.Message = None, *, reason = None):
        """
        Mark a suggestion as considered.
        """
        with open(r"./Data/DataBase/suggestions.json", "r") as f:
            suggestions = json.load(f)
        with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
            suggestion_log_channels = json.load(f)
        with open(r"./Data/DataBase/staff_roles.json", "r") as f:
            staff_roles = json.load(f)
        with open(r"./Data/DataBase/results.json", "r") as f:
            results = json.load(f)
        with open(r"./Data/DataBase/reasons.json", "r") as f:
            reasons = json.load(f)
        with open(r"./Data/DataBase/suggestors.json", "r") as f:
            suggesters = json.load(f)
        with open(r"./Data/DataBase/notes.json", "r") as f:
            notes = json.load(f)
        with open(r"./Data/DataBase/noters.json", "r") as f:
            noters = json.load(f)
        with open(r"./Data/DataBase/resulters.json","r") as f:
            resulters = json.load(f)
        if str(ctx.message.guild.id) not in staff_roles:
            embed = discord.Embed(
                title = "Ошибка Рассмотра",
                description = "Этот сервер не имеет роли персонала!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            staff_role_id = staff_roles[str(ctx.message.guild.id)]
            staff_role = discord.utils.get(ctx.message.author.roles, id = staff_role_id)
            if staff_role == None and ctx.message.author.guild_permissions.administrator == False:
                embed = discord.Embed(
                    title = "Ошибка Рассмотра",
                    description = f"Вам не хватает следующей роли: <@{staff_role_id}>!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if suggestion_id == None:
                    embed = discord.Embed(
                        title = "Ошибка Рассмотра",
                        description = "Пожалуйста напишите ID Предложения!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    suggestion_id = suggestion_id.id
                    if str(suggestion_id) not in suggestions:
                        embed = discord.Embed(
                            title = "Ошибка Рассмотра",
                            description = "Это неправильный ID!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
                    else:
                        resulters[str(suggestion_id)] = ctx.message.author.id
                        results[str(suggestion_id)] = "considered"
                        with open(r"./Data/DataBase/resulters.json", "w") as f:
                            json.dump(resulters, f, indent = 4)
                        with open(r"./Data/DataBase/results.json", "w") as f:
                            json.dump(results, f, indent = 4)
                        suggestion = suggestions[str(suggestion_id)]
                        suggestion_msg = await ctx.fetch_message(id = suggestion_id)
                        suggester = suggesters[str(suggestion_id)]
                        if str(suggestion_id) in notes:
                            noter = noters[str(suggestion_id)]
                            note = notes[str(suggestion_id)]
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Рассмотрен",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.considered
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Рассмотрен",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.considered
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        else:
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Рассмотрен",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.considered
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Рассмотрен",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.considered
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        with open(r"./Data/DataBase/reasons.json", "w") as f:
                            json.dump(reasons, f, indent = 4)
                        if str(ctx.message.guild.id) in suggestion_log_channels:
                            suggestion_log_channel = suggestion_log_channels[str(ctx.message.guild.id)]
                            suggestion_log_channel = discord.utils.get(ctx.guild.text_channels, id = suggestion_log_channel)
                            suggestion = suggestions[str(suggestion_id)]
                            if str(suggestion_id) in notes:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Рассмотренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.considered
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Рассмотренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.considered
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                            else:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Рассмотренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.considered
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Рассмотренное Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.considered
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)

    @commands.command()
    async def implement(self, ctx, suggestion_id : discord.Message = None, *, reason = None):
        """
        Mark a suggestion as implemented.
        """
        with open(r"./Data/DataBase/suggestions.json", "r") as f:
            suggestions = json.load(f)
        with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
            suggestion_log_channels = json.load(f)
        with open(r"./Data/DataBase/staff_roles.json", "r") as f:
            staff_roles = json.load(f)
        with open(r"./Data/DataBase/results.json", "r") as f:
            results = json.load(f)
        with open(r"./Data/DataBase/reasons.json", "r") as f:
            reasons = json.load(f)
        with open(r"./Data/DataBase/suggestors.json", "r") as f:
            suggesters = json.load(f)
        with open(r"./Data/DataBase/notes.json", "r") as f:
            notes = json.load(f)
        with open(r"./Data/DataBase/noters.json", "r") as f:
            noters = json.load(f)
        with open(r"./Data/DataBase/resulters.json","r") as f:
            resulters = json.load(f)
        if str(ctx.message.guild.id) not in staff_roles:
            embed = discord.Embed(
                title = "Ошибка Реализации",
                description = "Этот сервер не имеет роли персонала!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            staff_role_id = staff_roles[str(ctx.message.guild.id)]
            staff_role = discord.utils.get(ctx.message.author.roles, id = staff_role_id)
            if staff_role == None and ctx.message.author.guild_permissions.administrator == False:
                embed = discord.Embed(
                    title = "Ошибка Реализации",
                    description = f"Вам не хватает следующей роли: <@{staff_role_id}>!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if suggestion_id == None:
                    embed = discord.Embed(
                        title = "Ошибка Реализации",
                        description = "Пожалуйста напишите ID Предложения!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    suggestion_id = suggestion_id.id
                    if str(suggestion_id) not in suggestions:
                        embed = discord.Embed(
                            title = "Ошибка Реализации",
                            description = "Это неправильный ID!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
                    else:
                        resulters[str(suggestion_id)] = ctx.message.author.id
                        results[str(suggestion_id)] = "implemented"
                        with open(r"./Data/DataBase/resulters.json", "w") as f:
                            json.dump(resulters, f, indent = 4)
                        with open(r"./Data/DataBase/results.json", "w") as f:
                            json.dump(results, f, indent = 4)
                        suggestion = suggestions[str(suggestion_id)]
                        suggestion_msg = await ctx.fetch_message(id = suggestion_id)
                        suggester = suggesters[str(suggestion_id)]
                        if str(suggestion_id) in notes:
                            noter = noters[str(suggestion_id)]
                            note = notes[str(suggestion_id)]
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Реализовано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.implemented
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Реализовано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.implemented
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        else:
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Реализовано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.implemented
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = "no reason provided"
                            else:
                                embed = discord.Embed(
                                    title = "Реализовано",
                                    description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.implemented
                                )
                                embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                await suggestion_msg.edit(embed = embed)
                                reasons[str(suggestion_id)] = str(reason)
                        with open(r"./Data/DataBase/reasons.json", "w") as f:
                            json.dump(reasons, f, indent = 4)
                        if str(ctx.message.guild.id) in suggestion_log_channels:
                            suggestion_log_channel = suggestion_log_channels[str(ctx.message.guild.id)]
                            suggestion_log_channel = discord.utils.get(ctx.guild.text_channels, id = suggestion_log_channel)
                            suggestion = suggestions[str(suggestion_id)]
                            if str(suggestion_id) in notes:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Реализованое Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.implemented
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Реализованое Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}\n\n**Note by**\n<@{noter}>\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.implemented
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                            else:
                                if reason == None:
                                    embed = discord.Embed(
                                        title = "Реализованое Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.implemented
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)
                                else:
                                    embed = discord.Embed(
                                        title = "Реализованое Предложение",
                                        description = f"**Советчик**\n<@{suggester}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n{ctx.message.author.mention}\n\n**Reason**\n{reason}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.implemented
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_log_channel.send(embed = embed)

    @commands.command()
    async def note(self, ctx, suggestion_id : discord.Message = None, *, note = None):
        """
        Add a note to a suggestion.
        """
        with open(r"./Data/DataBase/suggestions.json", "r") as f:
            suggestions = json.load(f)
        with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
            suggestion_log_channels = json.load(f)
        with open(r"./Data/DataBase/staff_roles.json", "r") as f:
            staff_roles = json.load(f)
        with open(r"./Data/DataBase/results.json", "r") as f:
            results = json.load(f)
        with open(r"./Data/DataBase/reasons.json", "r") as f:
            reasons = json.load(f)
        with open(r"./Data/DataBase/suggestors.json", "r") as f:
            suggesters = json.load(f)
        with open(r"./Data/DataBase/notes.json", "r") as f:
            notes = json.load(f)
        with open(r"./Data/DataBase/noters.json", "r") as f:
            noters = json.load(f)
        with open(r"./Data/DataBase/resulters.json", "r") as f:
            resulters = json.load(f)
        if str(ctx.message.guild.id) not in staff_roles:
            embed = discord.Embed(
                title = "Note Error",
                description = "Этот сервер не имеет роли персонала!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            if suggestion_id == None:
                embed = discord.Embed(
                    title = "Note Error",
                    description = "Пожалуйста напишите ID Предложения!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                suggestion_id = suggestion_id.id
                if str(suggestion_id) not in suggestions:
                    embed = discord.Embed(
                        title = "Ошибка Примечания",
                        description = "Это неправильный ID!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    if note == None:
                        embed = discord.Embed(
                            title = "Ошибка Примечания",
                            description = "Please provide a note!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
                    else:
                        reason = reasons[str(suggestion_id)]
                        suggestion = suggestions[str(suggestion_id)]
                        suggestion_msg = await ctx.fetch_message(id = suggestion_id)
                        suggester = suggesters[str(suggestion_id)]
                        result = results[str(suggestion_id)]
                        if result == "pending":
                            embed = discord.Embed(
                                description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            embed.set_footer(text = f"ID Предложения {suggestion_id}")
                            await suggestion_msg.edit(embed = embed)
                            notes[str(suggestion_id)] = note
                            with open(r"./Data/DataBase/notes.json", "w") as f:
                                json.dump(notes, f, indent = 4)
                            noters[str(suggestion_id)] = str(ctx.message.author.id)
                            with open(r"./Data/DataBase/noters.json", "w") as f:
                                json.dump(noters, f, indent = 4)
                        else:
                            resulter = resulters[str(suggestion_id)]
                            if reason == "no reason provided":
                                if result == "approved":
                                    embed = discord.Embed(
                                        title = "Одобрено",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n<@{str(resulter)}>\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.approved
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                                if result == "denied":
                                    embed = discord.Embed(
                                        title = "Отказано",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n<@{str(resulter)}>\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.errorcolor
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                                if result == "considered":
                                    embed = discord.Embed(
                                        title = "Рассмотрен",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n<@{str(resulter)}>\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.considered
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                                if result == "implemented":
                                    embed = discord.Embed(
                                        title = "Реализовано",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n<@{str(resulter)}>\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.implemented
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                            else:
                                if result == "approved":
                                    embed = discord.Embed(
                                        title = "Одобрено",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Одобрено**\n<@{str(resulter)}>\n\n**Reason**\n{reason}\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.approved
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                                if result == "denied":
                                    embed = discord.Embed(
                                        title = "Отказано",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Отказано**\n<@{str(resulter)}>\n\n**Reason**\n{reason}\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.errorcolor
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                                if result == "considered":
                                    embed = discord.Embed(
                                        title = "Рассмотрен",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Рассмотрен**\n<@{str(resulter)}>\n\n**Reason**\n{reason}\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.considered
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)
                                if result == "implemented":
                                    embed = discord.Embed(
                                        title = "Реализован",
                                        description = f"**Советчик**\n<@{str(suggester)}>\n\n**Предложение**\n{suggestion}\n\n**Реализовано**\n<@{str(resulter)}>\n\n**Reason**\n{reason}\n\n**Note by**\n{ctx.message.author.mention}\n\n**Note**\n{note}",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.implemented
                                    )
                                    embed.set_footer(text = f"ID Предложения {suggestion_id}")
                                    await suggestion_msg.edit(embed = embed)
                                    notes[str(suggestion_id)] = note
                                    with open(r"./Data/DataBase/notes.json", "w") as f:
                                        json.dump(notes, f, indent = 4)
                                    noters[str(suggestion_id)] = str(ctx.message.author.id)
                                    with open(r"./Data/DataBase/noters.json", "w") as f:
                                        json.dump(noters, f, indent = 4)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def suggestionchannel(self, ctx, *, channel : discord.TextChannel = None):
        """
        Set which channel suggestions get sent to.
        """
        if channel == None:
            embed = discord.Embed(
                title = "Ошибка Каналов Предложений",
                description = "Пожалуйста, предоставьте канал логов!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            with open(r"./Data/DataBase/suggestion_channels.json", "r") as f:
                suggestion_channels = json.load(f)
            suggestion_channels[str(ctx.guild.id)] = channel.id
            embed = discord.Embed(
                title = "Канал Предложений",
                description = f"{ctx.message.guild}, канал с предложением поставлен: {channel.mention}",
                color = self.blurple
            )
            await ctx.send(embed = embed)
            with open(r"./Data/DataBase/suggestion_channels.json", "w") as f:
                json.dump(suggestion_channels, f, indent = 4)

    @suggestionchannel.error
    async def suggestionchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Отсутствуют Права",
                description = "Вам не хватает разрешения **Управление сервером**!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def suggestionlogchannel(self, ctx, *, channel : discord.TextChannel = None):
        """
        Set which channel suggestion logs get sent to.
        """
        if channel == None:
            embed = discord.Embed(
                title = "Ошибка Канала Журнала Предложений",
                description = "Пожалуйста, предоставьте канал логов!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            with open(r"./Data/DataBase/suggestion_log_channels.json", "r") as f:
                suggestion_log_channels = json.load(f)
            suggestion_log_channels[str(ctx.guild.id)] = channel.id
            embed = discord.Embed(
                title = "Канал Журнала Предложений",
                description = f"{ctx.message.guild}, канал с предложением сейчас {channel.mention}",
                color = self.blurple
            )
            await ctx.send(embed = embed)
            with open(r"./Data/DataBase/suggestion_log_channels.json", "w") as f:
                json.dump(suggestion_log_channels, f, indent = 4)

    @suggestionlogchannel.error
    async def suggestionlogchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Отсутствуют Права",
                description = "Вам не хватает разрешения **Управление сервером**!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def staffrole(self, ctx, *, role : discord.Role = None):
        """
        Set which role can accept / deny suggestions and etc.
        """
        if role == None:
            embed = discord.Embed(
                title = "Ошибка Роли Персонала",
                description = "Пожалуйста, укажите роль!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            with open(r"./Data/DataBase/staff_roles.json", "r") as f:
                staff_roles = json.load(f)
            staff_roles[str(ctx.guild.id)] = role.id
            embed = discord.Embed(
                title = "Роль Персонала",
                description = f"{ctx.message.guild}, роль персонала теперь такова {role.mention}",
                color = self.blurple
            )
            await ctx.send(embed = embed)
            with open(r"./Data/DataBase/staff_roles.json", "w") as f:
                json.dump(staff_roles, f, indent = 4)

    @staffrole.error
    async def staffrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Отсутствуют Права",
                description = "Вам не хватает разрешения **Управление сервером**!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Suggest(bot))

    #./Data/DataBase/