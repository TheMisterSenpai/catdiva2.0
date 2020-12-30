import discord
from discord.ext import commands
from discord.utils import get

import asyncio
import random
import youtube_dl
import string
import os

from googleapiclient.discovery import build
from module.catdivamodule import api

YOUTUBE_API = api.YOUTUBE_API

ytdl_format_options = {
    'audioquality':8,
    'format': 'worstaudio',
    'outtmpl': '{}',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    "extractaudio":True,
    "audioformat":"opus",
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' #bind to ipv4 since ipv6 addresses cause issues sometimes
}

stim = {
    'default_search': 'auto',
    "ignoreerrors":True,
    'quiet': True,
    "no_warnings": True,
    "simulate": True,  # do not keep the video files
    "nooverwrites": True,
    "keepvideo": False,
    "noplaylist": True,
    "skip_download": False,
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}


ffmpeg_options = {
    'options': '-vn',
    # 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}


class Downloader(discord.PCMVolumeTransformer):
    def __init__(self,source,*,data,volume=0.5):
        super().__init__(source,volume)
        self.data=data
        self.title=data.get('title')
        self.url=data.get("url")
        self.thumbnail=data.get('thumbnail')
        self.duration=data.get('duration')
        self.views=data.get('view_count')
        self.playlist={}

    @classmethod
    async def yt_download(cls,url,ytdl,*,loop=None,stream=False):
        """
        Download video directly with link
        """
        API_KEY = YOUTUBE_API
        youtube=build('youtube','v3',developerKey=API_KEY)
        data=youtube.search().list(part='snippet',q=url).execute()
        song_url=data
        song_info=data
        download= await loop.run_in_executor(None,lambda: ytdl.extract_info(song_url,download=not stream))
        filename=data['url'] if stream else ytdl.prepare_filename(download)
        return cls(discord.FFmpegPCMAudio(filename,**ffmpeg_options),data=download),song_info

    async def yt_info(self,song):
        """
        Get info from youtube
        """
        API_KEY='API_KEY'
        youtube=build('youtube','v3',developerKey=API_KEY)
        song_data=youtube.search().list(part='snippet').execute()
        return song_data[0]




    @classmethod
    async def video_url(cls,url,ytdl,*,loop=None,stream=False):
        """
        Download the song file and data
        """
        loop=loop or asyncio.get_event_loop()
        data= await loop.run_in_executor(None,lambda: ytdl.extract_info(url,download=not stream))
        data1={'queue':[]}
        if 'entries' in data:
            if len(data['entries']) >1:
                playlist_titles=[title['title'] for title in data['entries']]
                data1={'title':data['title'],'queue':playlist_titles}
                data1['queue'].pop(0)

            data=data['entries'][0]
                
        filename=data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename,**ffmpeg_options),data=data),data1



    async def get_info(self,url):
        """
        Get the info of the next song by not downloading the actual file but just the data of song/query
        """
        yt=youtube_dl.YoutubeDL(stim)
        down=yt.extract_info(url,download=False)
        data1={'queue':[]}
        if 'entries' in down:
            if len(down['entries']) > 1:
                playlist_titles=[title['title'] for title in down['entries']]
                data1={'title':down['title'],'queue':playlist_titles}

            down=down['entries'][0]['title']
            
        return down,data1


class MusicPlayer(commands.Cog):
    def __init__(self,client):
        self.bot=client
        # self.database = pymongo.MongoClient(os.getenv('MONGO'))['Discord-Bot-Database']['General']
        # self.music=self.database.find_one('music')
        self.player={
            "audio_files":[]
        }
        self.cog_name = ['музыка']

    @property
    def random_color(self):
        return discord.Color.from_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))

    # def cog_unload(self):
    #     """
    #     Update the database in mongodb to the latest changes when the bot is disconnecting
    #     """
    #     current=self.database.find_one('music')
    #     if current != self.voice:
    #         self.database.update_one({'_id':'music'},{'$set':self.music})



    @commands.Cog.listener('on_voice_state_update')
    async def music_voice(self,user,before,after):
        """
        Clear the server's playlist after bot leave the voice channel
        """
        if after.channel is None and user.id == self.bot.user.id:
            try:
                self.player[user.guild.id]['queue'].clear()
            except KeyError:
                #NOTE: server ID not in bot's local self.player dict
                print(f"Failed to get guild id {user.guild.id}") #Server ID lost or was not in data before disconnecting



    async def filename_generator(self):
        """
        Generate a unique file name for the song file to be named as
        """
        chars=list(string.ascii_letters+string.digits)
        name=''
        for i in range(random.randint(9,25)):
            name+=random.choice(chars)
        
        if name not in self.player['audio_files']:
            return name

        
        return await self.filename_generator()


    async def playlist(self,data,msg):
        """
        THIS FUNCTION IS FOR WHEN YOUTUBE LINK IS A PLAYLIST
        Add song into the server's playlist inside the self.player dict 
        """
        for i in data['queue']:
            self.player[msg.guild.id]['queue'].append({'title':i,'author':msg})



    async def queue(self,msg,song):
        """
        Add the query/song to the queue of the server
        """
        title1=await Downloader.get_info(self,url=song)
        title=title1[0]
        data=title1[1]
        #NOTE:needs fix here
        if data['queue']:
            await self.playlist(data,msg)
            #NOTE: needs to be embeded to make it better output
            return await msg.send(f"Добавлена музыка {data['title']} в очередь")
        self.player[msg.guild.id]['queue'].append({'title':title,'author':msg})
        return await msg.send(f"**{title} добавлена в очередь**".title())



    async def voice_check(self,msg):
        """
        function used to make bot leave voice channel if music not being played for longer than 2 minutes
        """
        if msg.voice_client is not None:
            await asyncio.sleep(120)
            if msg.voice_client is not None and msg.voice_client.is_playing() is False and msg.voice_client.is_paused() is False:
                await msg.voice_client.disconnect()


    async def clear_data(self,msg):
        """
        Clear the local dict data
            name - remove file name from dict
            remove file and filename from directory
            remove filename from global audio file names
        """
        name=self.player[msg.guild.id]['name']
        os.remove(name)
        self.player['audio_files'].remove(name)


    async def loop_song(self,msg):
        """
        Loop the currently playing song by replaying the same audio file via `discord.PCMVolumeTransformer()`
        """
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.player[msg.guild.id]['name']))
        loop=asyncio.get_event_loop()
        try:
            msg.voice_client.play(source, after=lambda a: loop.create_task(self.done(msg)))
            msg.voice_client.source.volume=self.player[msg.guild.id]['volume']
            # if str(msg.guild.id) in self.music:
            #     msg.voice_client.source.volume=self.music['vol']/100
        except Exception as Error:
            #Has no attribute play
            print(Error) #NOTE: output back the error for later debugging


    async def done(self,msg,msgId:int=None):
        """
        Function to run once song completes
        Delete the "Now playing" message via ID
        """
        if msgId:
            try:
                message=await msg.channel.fetch_message(msgId)
                await message.delete()
            except Exception as Error:
                print("Failed to get the message")

        if self.player[msg.guild.id]['reset'] is True:
            self.player[msg.guild.id]['reset']=False
            return await self.loop_song(msg)

        if msg.guild.id in self.player and self.player[msg.guild.id]['repeat'] is True:
            return await self.loop_song(msg)

        await self.clear_data(msg)

        if self.player[msg.guild.id]['queue']:
            queue_data=self.player[msg.guild.id]['queue'].pop(0)
            return await self.start_song(msg=queue_data['author'],song=queue_data['title'])


        else:
            await self.voice_check(msg)
    

    async def start_song(self,msg,song):
        new_opts=ytdl_format_options.copy()
        audio_name=await self.filename_generator()

        self.player['audio_files'].append(audio_name)
        new_opts['outtmpl']=new_opts['outtmpl'].format(audio_name)

        ytdl=youtube_dl.YoutubeDL(new_opts)
        download1=await Downloader.video_url(song,ytdl=ytdl,loop=self.bot.loop)

        download=download1[0]
        data=download1[1]
        self.player[msg.guild.id]['name']=audio_name
        emb=discord.Embed(colour=self.random_color, title='Сейчас играет',description=download.title,url=download.url)
        emb.set_thumbnail(url=download.thumbnail)
        emb.set_footer(text=f'Запрошено {msg.author.display_name}',icon_url=msg.author.avatar_url)
        loop=asyncio.get_event_loop()




        if data['queue']:
            await self.playlist(data,msg)

        msgId=await msg.send(embed=emb)
        self.player[msg.guild.id]['player']=download
        self.player[msg.guild.id]['author']=msg
        msg.voice_client.play(download,after=lambda a: loop.create_task(self.done(msg,msgId.id)))

        # if str(msg.guild.id) in self.music: #NOTE adds user's default volume if in database
        #     msg.voice_client.source.volume=self.music[str(msg.guild.id)]['vol']/100
        msg.voice_client.source.volume=self.player[msg.guild.id]['volume']
        return msg.voice_client



    @commands.command(
    	aliases=['играть', 'pl'],
        description='включает любую музыку',
        usage='играть <ссылка на ютуб> или <Исполнитель - название музыки>'
    	)
    async def play(self,msg,*,song):
        
        if msg.guild.id in self.player:
            if msg.voice_client.is_playing() is True:#NOTE: SONG CURRENTLY PLAYING
                return await self.queue(msg,song)

            if self.player[msg.guild.id]['queue']:
                return await self.queue(msg,song)

            if msg.voice_client.is_playing() is False  and not self.player[msg.guild.id]['queue']:
                return await self.start_song(msg,song)


        else:
            #IMPORTANT: THE ONLY PLACE WHERE NEW `self.player[msg.guild.id]={}` IS CREATED
            self.player[msg.guild.id]={
                'player':None,
                'queue':[],
                'author':msg,
                'name':None,
                "reset":False,
                'repeat':False,
                'volume': 0.5
            }
            return await self.start_song(msg,song)


    @play.before_invoke
    async def before_play(self,msg):
    
        if msg.author.voice is None:
            return await msg.send('**Пожалуйста, присоединитесь к голосовому чату чтобы включить музыку**'.title())

        if msg.voice_client is None: 
            return await msg.author.voice.channel.connect()


        if msg.voice_client.channel != msg.author.voice.channel:
            
            #NOTE: Check player and queue 
            if msg.voice_client.is_playing() is False and not self.player[msg.guild.id]['queue']:
                return await msg.voice_client.move_to(msg.author.voice.channel)
                #NOTE: move bot to user's voice channel if queue does not exist
            
            if self.player[msg.guild.id]['queue']:
                #NOTE: user must join same voice channel if queue exist
                return await msg.send("Пожалуйста, зайдите в тот же голосовой чат, что и бот, чтобы добавить музыку в очередь")
            
    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['повторить', 'rt'],
        description='повторить музыку',
        usage='повторить'
    	)
    async def repeat(self,msg):
        if msg.guild.id in self.player:
            if msg.voice_client.is_playing() is True:
                if self.player[msg.guild.id]['repeat'] is True:
                    self.player[msg.guild.id]['repeat']=False
                    return await msg.message.add_reaction(emoji='✅')
                    
                self.player[msg.guild.id]['repeat']=True
                return await msg.message.add_reaction(emoji='✅')

            return await msg.send("Сейчас ничего не играет")
        return await msg.send("Бот не в голосовом чате или не проигрывает музыку")

    @repeat.error
    async def repeat_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)

    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['перезапустить', 'rst'],
        description='перезапустить музыку',
        usage='перезапустить'
    	)
    async def reset(self,msg):
        if msg.voice_client is None:
            return await msg.send(f"**{msg.author.display_name}, в данный момент бот не проигрывает никакую музыку.**")

        if msg.author.voice is None or msg.author.voice.channel != msg.voice_client.channel:
            return await msg.send(f"**{msg.author.display_name}, вы должны быть в том же голосовом канале что и бот.**")

        if self.player[msg.guild.id]['queue'] and msg.voice_client.is_playing() is False:
            return await msg.send("**Никакая музыка сейчас не играет или нет музыки в очереди**".title(),delete_after=25)

        self.player[msg.guild.id]['reset']=True
        msg.voice_client.stop()

    @reset.error
    async def reset_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)  
            

    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['пропустить', 'sp'],
        description='пропустить музыку',
        usage='пропустить'
    	)
    async def skip(self,msg):
        if msg.voice_client is None:
            return await msg.send("**Никакая музыка сейчас не играет**".title(),delete_after=60)

       
        if msg.author.voice is None or msg.author.voice.channel != msg.voice_client.channel:
            return await msg.send("Пожалуйста, зайдите в тот же голосовой канал то и бот")
        
        
        if self.player[msg.guild.id]['queue'] and msg.voice_client.is_playing() is False:
            return await msg.send("**Нечего пропускать потому что в очереди нет музыки**".title(),delete_after=60)


        self.player[msg.guild.id]['repeat']=False
        msg.voice_client.stop()
        return await msg.message.add_reaction(emoji='✅')

    @skip.error
    async def skip_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)  

    
    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['остановить'],
        description='остановить музыку',
        usage='остановить'
    	)
    async def stop(self,msg):
        if msg.voice_client is None:
            return await msg.send("Бот не подключён к голосовому каналу")

        if msg.author.voice is None:
            return await msg.send("Вы должны быть в том же голосовом чате что и бот")

        if msg.author.voice is not None and msg.voice_client is not None:
            if  msg.voice_client.is_playing() is True or self.player[msg.guild.id]['queue']:
                self.player[msg.guild.id]['queue'].clear()
                self.player[msg.guild.id]['repeat']=False
                msg.voice_client.stop()
                return await msg.message.add_reaction(emoji='✅')

            return await msg.send(f"**{msg.author.display_name}, Никакая музыка сейчас не играет или нет музыки в очереди**")

    @stop.error
    async def stop_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)       


    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['выйти', 'lv'],
        description='выйти с голового чата',
        usage='выйти'
	)
    async def leave(self,msg):
        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_playing() is True or self.player[msg.guild.id]['queue']:
                self.player[msg.guild.id]['queue'].clear()
                msg.voice_client.stop()
                return await msg.voice_client.disconnect(), await msg.message.add_reaction(emoji='✅')
            
            return await msg.voice_client.disconnect(), await msg.message.add_reaction(emoji='✅')
        
        if msg.author.voice is None:
            return await msg.send("Вы должны быть в том же голосовом канале что и бот для отключения его же через команду")

    @leave.error
    async def leave_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)


    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['пауза', 'pe'],
        description='поставить на паузу музыку',
        usage='пауза'
    	)
    async def pause(self,msg):
        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_paused() is True:
                return await msg.send("Музыка уже на паузе")

            if msg.voice_client.is_paused() is False:
                msg.voice_client.pause()
                await msg.message.add_reaction(emoji='✅')

    @pause.error
    async def _хентай_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)

    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['продолжить', 're'],
        description='возобновить музыку',
        usage='продолжить'
    	)
    async def resume(self,msg):
        if msg.author.voice is not None and msg.voice_client is not None:
            if msg.voice_client.is_paused() is False:
                return await msg.send("Музыка уже играет")

            if msg.voice_client.is_paused() is True:
                msg.voice_client.resume()
                return await msg.message.add_reaction(emoji='✅')

    @resume.error
    async def resume_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)


    @commands.command(
    	aliases=['очередь', 'queue'],
        description='узнать очередь на музыку',
        usage='очередь'
    	)
    async def _queue(self,msg):
        if msg.voice_client is not None:
            if msg.guild.id in self.player:
                if self.player[msg.guild.id]['queue']:
                    emb=discord.Embed(colour=self.random_color, title='очередь')
                    emb.set_footer(text=f'Команда, использованная {msg.author.name}',icon_url=msg.author.avatar_url)
                    for i in self.player[msg.guild.id]['queue']:
                        emb.add_field(name=f"**{i['author'].author.name}**",value=i['title'],inline=False)
                    return await msg.send(embed=emb,delete_after=120)

        return await msg.send("В очереди нет музыки")

    @_queue.error
    async def _queue_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)           


    @commands.command(
    	aliases=['музыка?', 's_i'],
        description='получить информацию о музыке',
        usage='музыка?'
    	)
    async def song_info(self,msg):
        if msg.voice_client is not None and msg.voice_client.is_playing() is True:
            emb=discord.Embed(colour=self.random_color, title='Сейчас играет',description=self.player[msg.guild.id]['player'].title)
            emb.set_footer(text=f"{self.player[msg.guild.id]['author'].author.name}",icon_url=msg.author.avatar_url)
            emb.set_thumbnail(url=self.player[msg.guild.id]['player'].thumbnail)
            return await msg.send(embed=emb,delete_after=120)
        
        return await msg.send(f"**Сейчас не играет никакая музыка**".title(),delete_after=30)

    @song_info.error
    async def song_info_error( self, ctx, error ):
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)


    @commands.command(
    	aliases=['присоед', 'jn'],
        description='присоединить бота к голосовому чату',
        usage='присоед'
    	)
    async def join(self, msg, *, channel: discord.VoiceChannel=None):
        if msg.voice_client is not None:
            return await msg.send(f"Бот уже в голосовом канале\nВы хотели использовать {msg.prefix}перейти в")

        if msg.voice_client is None:
            if channel is None:
                return await msg.author.voice.channel.connect(), await msg.message.add_reaction(emoji='✅')
            
            return await channel.connect(), await msg.message.add_reaction(emoji='✅')
        
        else:
            if msg.voice_client.is_playing() is False and not self.player[msg.guild.id]['queue']:
                return await msg.author.voice.channel.connect(), await msg.message.add_reaction(emoji='✅')


    @join.before_invoke
    async def before_join(self,msg):
        if msg.author.voice is None:
            return await msg.send("Вы не в голосовом канале")



    @join.error
    async def join_error(self,msg,error):
        if isinstance(error,commands.BadArgument):
            return msg.send(error)

        if error.args[0] == 'Команда вызвала исключение: исключение: играет':
            return await msg.send("**Пожалуйста, зайдите в тот же голосовой чат что и бот для того, что бы добавить музыку в очередь**".title())

        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)


    @commands.has_permissions(manage_channels=True)
    @commands.command(
    	aliases=['громкость', 've'],
        description='установить громкость на музыку',
        usage='громкость <1-200>'
    	)
    async def volume(self,msg,vol:int):
        
        if vol > 200:
            vol = 200
        vol=vol/100
        if msg.author.voice is not None:
            if msg.voice_client is not None:
                if msg.voice_client.channel == msg.author.voice.channel and msg.voice_client.is_playing() is True:
                    msg.voice_client.source.volume=vol
                    self.player[msg.guild.id]['volume']=vol
                    # if (msg.guild.id) in self.music:
                    #     self.music[str(msg.guild.id)]['vol']=vol
                    return await msg.message.add_reaction(emoji='✅')
                    
        
        return await msg.send("**Пожалуйста, зайдите в тот же голосовой канал, что и бот, что бы использовать команду**".title(),delete_after=30)
    

    
    @volume.error
    async def volume_error(self,msg,error):
        if isinstance(error,commands.MissingPermissions):
            return await msg.send("Для изменения громкости необходимы права администратора",delete_after=30)   
        if isinstance( error, commands.errors.CommandInvokeError ):
            emb = discord.Embed(colour = discord.Color.red())
            emb.add_field( name = 'Ошибка:', value = '❗️ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций' ) 
            await ctx.send( embed = emb)

def setup(bot):
    bot.add_cog(MusicPlayer(bot))            