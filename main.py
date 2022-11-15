import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import requests
import time
import os
from dotenv import load_dotenv
import youtube_dl

load_dotenv()





intents = discord.Intents.default()
intents.message_content = True
# intents = discord.Intents().all()
# client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='§', intents=intents)


token = os.getenv('DISCORD_BOT_TOKEN')
openweather_apikey = os.getenv('OPENWEATHER_APIKEY')
windy_apikey = os.getenv('WINDY_APIKEY')
# webcamid = "1447838456"
webcamid = "1665493001"
alarm_msg = "https://tenor.com/view/danger-alert-siren-alarm-red-light-gif-16931369"

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# @bot.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == "Duisburg-Calais Logistics":
            for channel in guild.text_channels :
                if str(channel) == "die-einzig-wahren-memez" :
                    await channel.send("MichaelScottBot is online. That's what she said!")
                    await channel.send(file=discord.File('michaelScottBot.gif'))
            print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))


@bot.command(help = "Prints details of Server")
async def server_info(ctx):
    for guild in bot.guilds:
        owner=str(guild.owner)
        # region = str(guild.region)
        guild_id = str(guild.id)
        memberCount = str(guild.member_count)
        # icon = str(guild.icon_url)
        desc=guild.description
           
        embed = discord.Embed(
            title=guild.name + " Server Information",
            description=desc,
            color=discord.Color.blue()
        )
        # embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        # embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

        members=[]
        async for member in ctx.guild.fetch_members(limit=150) :
            await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))




@bot.command(pass_context = True)
async def spam(ctx, *args):  
        error = 'Command: §spam [user-id] [int] [body]; \n[user-id] --> Mention User with @; \n[int] --> amount beeing sent. Limit = 100; \n[body] --> custom message / default: Alarm '
        if len(args) != 0:
            if args[0] == "help":
                await ctx.channel.send(f'{ctx.author.mention} '+ error)

            if len(args) >= 2:
                try:
                    await ctx.channel.send(f'{ctx.author.mention} Spam started!')
                    username = args[0]
                    uname = username[2:len(username)-1]
                    user = await bot.fetch_user(uname)
                    msg = alarm_msg
    
                    if len(args) >= 3:
                        msg = args[2]
                    
                    amount = int(args[1])
                    if amount >= 100:
                        amount = 100
                    
                    i = 0
                    while(i < amount):
                        await user.send(msg)
                        i = i + 1
                        time.sleep(0.25)
                    await ctx.channel.send(f'{ctx.author.mention} Spam complete: '+ str(amount))
                except:
                    await ctx.channel.send(f'{ctx.author.mention} Spamed user has to be in text channel!')
        else:
           await ctx.channel.send(f'{ctx.author.mention} Invalid command. Use this: \n'+error) 



@bot.command(pass_context = True)
async def nordpol(ctx):
        nweather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat=90&lon=135&appid={openweather_apikey}&units=metric')
        windy = requests.get(f'https://api.windy.com/api/webcams/v2/list/webcam={webcamid}?show=webcams:image&key={windy_apikey}')
        weather = nweather.json()
        windyj = windy.json()
        print(windyj)
        temp = weather['main']['temp']
        feels_like = weather['main']['feels_like']
        northpoleimg = windyj['result']['webcams'][0]['image']['current']['preview']
        await ctx.channel.send(f'{northpoleimg}\n{ctx.author.mention} Die aktuellen Temperaturen am Nordpol lauten: {temp}°C Gefühlt: {feels_like}°C')


songs_list = []
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

async def play_next(ctx):
    if len(songs_list) == 1:
        songs_list.pop(0)
        await ctx.send("No more Songs to skip.")
        return
    elif len(songs_list) < 1:
        await ctx.send("No more Songs to skip.")
        return
    else:
        songs_list.pop(0)
       
    await ctx.send("Waiting on next song...")
    
    try:
        if os.path.isfile("song.mp3"):
            os.remove("song.mp3")
    except PermissionError:
        print("permissionerror")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([songs_list[0]])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):  
            os.rename(file, "song.mp3")
                
    voice = get(bot.voice_clients, guild=ctx.guild)
    # voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: play_next(ctx))
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    await ctx.send("Playing Song ⏯️")


@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.channel.send(f'{ctx.author.mention} You need to be in a voice channel to call me!')
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.channel.send(f'{ctx.author.mention} Joined Voice Channel: {channel}')


@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url: str):
    if len(songs_list) <= 0:
        songs_list.append(url)
        await ctx.send("Waiting on song...")
    else:
        songs_list.append(url)
        await ctx.channel.send(f'{ctx.author.mention} Your song has been added to the queue.')
        return
        
    
    
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.channel.send(f'{ctx.author.mention} You are not connected to a voice channel!')
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    
    try:
        if os.path.isfile("song.mp3"):
            os.remove("song.mp3")
    except PermissionError:
        print("permissionerror")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([url])
        ydl.download([songs_list[0]])
        
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    await ctx.channel.send(f'{ctx.author.mention} Playing Song ⏯️')



@bot.command(description="skip music")
async def skip(ctx):
    await ctx.channel.send(f'{ctx.author.mention} Song skiped!')
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await voice.disconnect(force=True)
    voice.cleanup()


    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.channel.send(f'{ctx.author.mention} You are not connected to a voice channel!')
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    
    await play_next(ctx)
    

@bot.command(description="stop music")
async def stop(ctx):
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.stop()
    await voice.disconnect(force=True)
    voice.cleanup()

    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.channel.send(f'{ctx.author.mention} You are not connected to a voice channel!')
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.channel.send(f'{ctx.author.mention} Song Stoped!')
    

@bot.command(description="pauses music")
async def pause(ctx):
    ctx.voice_client.pause()
    await ctx.channel.send(f'{ctx.author.mention} Paused ⏸️')
    
@bot.command(description="resumes music")
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.channel.send(f'{ctx.author.mention} Resuming ⏯️')

@bot.command(description="queue skiped")
async def skipq(ctx):
    songs_list.clear()
    await ctx.channel.send(f'{ctx.author.mention} Queue skiped!')

@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.channel.send(f'{ctx.author.mention} Left Channel: {channel}')
    else:
        await ctx.channel.send(f'{ctx.author.mention} Do not think I am in a voice channel!')


if(os.getenv('DEPLOY_STATE') == 'true'):
    bot.run(token)