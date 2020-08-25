import discord
from discord.ext import commands
from discord.utils import get

class administration(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions( administrator = True) 
    async def clear( self, ctx, amount : int ):
	    await ctx.channel.purge( limit = amount )

	    await ctx.send(f'``✔️Удаленно {amount} сообщений``')
	    await ctx.channel.purge( limit = 1) 

    @commands.command( pass_context = True)
    @commands.has_permissions( administrator = True)
    async def kick( self, ctx, member: discord.Member, *, reason = None ):
	    await ctx.channel.purge( limit = 1)

	    await member.kick( reason = reason )
	    await ctx.message( f'Был кикнут {member.mention}')

    @commands.command( pass_context = True)
    @commands.has_permissions( administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
	    await ctx.channel.purge( limit = 1)

	    await member.ban( reason = reason)
	    await ctx.send(f'Был заблокирован {member.mention}')

    @commands.command( pass_context = True)
    @commands.has_permissions( administrator = True)
    async def unban ( self, ctx, *, member):
	    await ctx.channel.purge( limit = 1)
	    banned_users = await ctx.guild.bans()

	    for ban_entry in banned_users:
		    user = ban_entry.user # User#1234

		    await ctx.guild.unban( user )
		    await ctx.send( f'Был разблокирован { user.mention}' )

		    return

    @commands.command()
    async def report(self, ctx, member:discord.Member=None, *, arg=None):
        message = ctx.message
        channel = client.get_channel(692978927781806121)    
        if member == None:
            await ctx.send(embed=discord.Embed(description='Укажите пользователя!', color=discord.Color.red()))
        elif arg == None:
            await ctx.send(embed=discord.Embed(description='Укажите причину жалобы!', color=discord.Color.red()))
        else:
            emb = discord.Embed(title=f'Жалоба на пользователя {member}', color=discord.Color.blue())
            emb.add_field(name='Автор жалобы:', value=f'*{ctx.author}*')
            emb.add_field(name='Причина:', value='*' +arg + '*')
            emb.add_field(name='ID жалобы:', value=f'{message.id}')
            await channel.send(embed=emb)
            await ctx.author.send('✅ Ваша жалоба успешно отправлена!')            

    @commands.Cog.listener()
    async def on_ready(self):
        print('[LOG] загружен administration.py')       

def setup(client):
    client.add_cog(administration(client)) 