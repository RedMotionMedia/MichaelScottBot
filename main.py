
from ast import arg
from queue import Empty
from discord.ext import commands
import discord
import requests
import time

# client = discord.Client()
bot = commands.Bot(command_prefix='§')
token = "OTYwNTE3MDc2MzMyNzA3OTcy.YkrlPA.dH9YnklhY7SuwvmNZbdGZ1Rocj0"
openweather_apikey = "8112867c5131111875b74070e5599e38"
windy_apikey = "TUuK42PhI7aJD0Rm2MSDhnB7IMqm5bqy"
# webcamid = "1447838456"
webcamid = "1665493001"
alarm_msg = "https://tenor.com/view/danger-alert-siren-alarm-red-light-gif-16931369"



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))



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



@bot.command(pass_context = True)
async def join(ctx):
    try:
        if type(ctx.author.voice) == type(None):
            await ctx.channel.send(f'{ctx.author.mention} Du musst in einem Voice Channel sein um mich einzuladen!')
        else:
            vchannel = ctx.author.voice.channel
            voice = await vchannel.connect()
            await ctx.channel.send(f'{ctx.author.mention} Joined Voice Channel')
    except:
       await ctx.channel.send(f'{ctx.author.mention} Es ist etwas schief gelaufen!')

    


@bot.command(pass_context = True)
async def leave(ctx):
    await ctx.voice_client.disconnect()


bot.run(token)




# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')


# client.run(token)