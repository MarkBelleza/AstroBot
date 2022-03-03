import discord
import os        #neded for taking the token 
from keep_alive import keep_alive      #needed for keeping the bot alive (pings the bot)
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '>')

mark = [] #my inbox


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online,     activity=discord.Game("creator: Light"))
  print('ASTRO_BOT STATUS: ONLINE')

@client.command(aliases=['hello', 'Hello', 'HELLO'])
async def hi(ctx):
  message_author = str(ctx.author)
  if (message_author == "Light#5080"):
    await ctx.send("Hello Master!")
  elif (message_author == "JΛY#9372"):
    await ctx.send("Hi Bitch")
  elif (message_author == "hunhan#1081"):
    await ctx.send("Hello hunhan!")
  elif (message_author == "SsugareB#6693"):
    await ctx.send("Hello Jezrel!")
  elif (message_author == "K.Irvin27#9556"):
    await ctx.send("Hello handsome")
  elif (message_author == "Nenn#5067"):
    await ctx.send("wassup pu#%sy")
  elif (message_author == "๖ۣۣۜRed#0001"):
    await ctx.send("watchu lookin at")
  elif (message_author == "Moonlit6224#3574"):
    await ctx.send("Jollibee evening, are you staying Jolly?")
  elif (message_author == "MarkU#7285"):
    await ctx.send("Hi daddy Mark, stay fragging okey?")
  elif (message_author == "yuuta#0005"):
    await ctx.send("Hi Yuuta, stay excellent and be brave!")
  elif (message_author == "Antiwan#3720"):
    await ctx.send("Hi Sir, bend over right now")
  else:
    await ctx.send('hello')


@client.command(aliases= ['box'])
async def _inbox(ctx):
  messages = str(len(mark))
  await ctx.send(messages + " message(s)")

@client.command(aliases= ['send'])
async def _send(ctx, *, message):
  mark.append(message)
  await ctx.message.delete()

@client.command(aliases= ['read'])
async def _open(ctx):
  mes = str(mark.pop())
  await ctx.send("anonymous: " + mes)
  
  
  
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = ['It is Certain.', 
              'It is decidedly so.',
              'Without a doubt.',
              'Yes definitely.',
              'You may rely on it.',
              'As I see it, yes.',
              'Most likely.',
              'Outlook good.',
              'Yes.',
              'Signs point to yes.',
              'Reply hazy, try again.',
              'Ask again later.',
              'Better not tell you now.',
              'Cannot predict now.',
              'Concentrate and ask again.',
              "Don't count on it.",
              'My reply is no.',
              'My sources say no.',
              'Outlook not so good.',
              'Very doubtful.']
  await ctx.send(random.choice(responses))

@client.command()
async def say(ctx, *, repeat):
  await ctx.send(repeat)

@client.event
async def on_message_delete(message):
  message_author = str(message.author)
  
  if (not (">send" in message.content)):
    
    chan2 = client.get_channel(945143392667570236) #pepe
    chan3 = client.get_channel(946986698166923295) #geng
  
    await chan2.send("AUTHOR: " + message_author + "\n" + "MESSAGE:\n" + message.content)
    await chan3.send("AUTHOR: " + message_author + "\n" + "MESSAGE:\n" + message.content)
  
  else:
    print("sent")



keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)



