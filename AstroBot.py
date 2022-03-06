import discord
import os        #neded for taking the token 
from keep_alive import keep_alive      #needed for keeping the bot alive (pings the bot)
from discord.ext import commands
import random
import copy

roster = {} #inboxes
in_game = {} #players in game
queue = [] #invites sent


client = commands.Bot(command_prefix = '>')

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
    await ctx.send("Wassup meeen")
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

      
#initialize inbox
@client.command(aliases= ['mkbox'])
async def _mkinbox(ctx):
  author = str(ctx.author)
  if (not (author in roster)):
    roster[author] = []
  else:
    await ctx.send("Inbox already exist")

#how many messages
@client.command(aliases= ['box'])
async def _inbox(ctx):
  author = str(ctx.author)
  if (author in roster):
    messages = str(len(roster[author]))
    await ctx.send(messages + " message(s)")
  else:
    await ctx.send("Inbox does not exist")
    
#send messages
@client.command(aliases= ['send'])
async def _send(ctx, *, message):
  author = message.split(' ', 1)[0]
  if (author in roster):
    roster[author].append(message.split(' ', 1)[1])
  await ctx.message.delete()
  
#read messages
@client.command(aliases= ['read'])
async def _open(ctx):
  author = str(ctx.author)
  if (author in roster):
    message = str(roster[author].pop())
    await ctx.send("anonymous: " + message)

#8ball
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

#TIC TAC TOE game--------------------------------------------------------------------------
#default board
x = [['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'], 
     0]

#print current board
def printB(key):
  board = '``` '
  for i in range (len(in_game[key]) - 1):
      for j in range (len(in_game[key][0])):
          if (j != 2):
            board = board + str(in_game[key][i][j]) + '  |  '
          else:
            board = board + str(in_game[key][i][j])
      if (i != 2):
        board = board + "\n "
  board = board + ' ```'
  return board

@client.command(aliases=['t'])
async def TTT(ctx, key):
  await ctx.send(printB(key))

#Player makes a move
@client.command(aliases=['tic', 'tac', 'toe'])
async def turn(ctx, key, spot):
  spot = (int(spot))
  player = str(ctx.author)
  pos = ()
  win_condition = False
  
  if ((spot >= 1) & (spot <= 3)):
    pos = (0, (spot - 1))
  elif ((spot >= 4) & (spot <= 6)):
    pos = (1, (spot - 4))
  elif ((spot >= 7) & (spot <= 9)):
    pos = (2, (spot - 7))
  else:
    await ctx.send('invalid spot')
    return False
    
  if (player in str(key)):
    if (in_game[key][3] % 2 == 0):          #even, 0,2,4...
      in_game[key][pos[0]][pos[1]] = 'O'
      print(x)
      win_condition = check_board(pos, 'O', key)
    else:                                   #odd, 1,3,5...
      in_game[key][pos[0]][pos[1]] = 'X'
      win_condition = check_board(pos, 'X', key)
    in_game[key][3] += 1 
    
  if win_condition:
    await ctx.send(printB(key))
    await ctx.send('Total Moves: ' + str(in_game[key][3]))
    await ctx.send(str(ctx.author) + 'Wins!')
    in_game.pop(key)
  else:
    await ctx.send(printB(key))
    await ctx.send('Total Moves: ' + str(in_game[key][3]))
    await ctx.send('Key: ' + key)

  
#Check for win condition----------------------------------------------------------
def check_board(pos, letter, key):
  board = in_game[key]
  row = check_row(pos, letter, board)
  col = check_col(pos, letter, board)
  diag = check_diagonal(pos, letter, board)
  
  if (row or col or diag):
    return True
  else:
    return False

#Check row
def  check_row(pos, letter, board):
  for i in range(len(board[0])):
    if (board[pos[0]][i] != letter):
      return False
  return True
  
#Check col
def check_col(pos, letter, board):
  for j in range(len(board) - 1):
    if (board[j][pos[1]] != letter):
      return False
  return True

#Check diagonal
def check_diagonal(pos, letter, board):
  diagonal1 = [board[i][i] for i in range(len(board[0]))]
  diagonal2 = [board[i][len(board[0]) - 1 - i] for i in range(len(board[0]))]

  if (((pos[0] == 0) & (pos[1] == 0)) | ((pos[0] == 2) & (pos[1] == 2))):
    for i in range (len(diagonal1)):
      if diagonal1[i] != letter:
        return False
  else:
    for j in range (len(diagonal2)):
      if diagonal2[j] != letter:
        return False
  return 
#--------------------------------------------------------------------------------------------
#INVITING AND ACCEPTING------------------------------------------------------------
#INVITE
@client.command(aliases = ['i', 'inv', 'invite'])
async def send_invite(ctx, invite):
  author = str(ctx.author)
  key = author + str(invite)
  if (not(key in queue)):
    queue.append(key)
  else:
    await ctx.send("already sent an invite to " + invite)

#ACCEPT 
@client.command(aliases = ['k', 'okey', 'accept'])
async def _accept(ctx, host):
  author = str(ctx.author)
  key = str(host) + author
  if (key in queue):
    queue.remove(key)
    in_game[key] = copy.deepcopy(x)
    await ctx.send('KEY: ' + key)
    await ctx.send(printB(key))
  else:
    await ctx.send(host + " has not given you an invite")

#DECLINE 
@client.command(aliases = ["n, no, decline"])
async def _decline(ctx, host):
  author = str(ctx.author)
  key = str(host) + author
  if (key in queue):
    queue.remove(key)
  else:
    await ctx.send(host + " has not given you an invite")
#-------------------------------------------------------------------------------------------
#Tic Tac Toe Game END HERE ----



    
#ADMIN COMMANDS ************************************************************
admin_key = "199597758741479425"

#check current roster
@client.command(aliases= ['roster'])
async def check_roster(ctx):
  if (str(ctx.author.id) == admin_key):
    await ctx.send('roster: ' + str(roster.keys())[9:])

#remove inbox
@client.command(aliases= ['remove'])
async def remove_from_roster(ctx, name):
  if (str(ctx.author.id) == admin_key):
    if (name in roster):
      roster.pop(name)
      await ctx.send(name + " removed")
      
#check current queue
@client.command(aliases= ['q', 'queue'])
async def check_queue(ctx):
  if (str(ctx.author.id) == admin_key):
    await ctx.send('players in queue ' + str(queue))

#check current in_game
@client.command(aliases= ['ingame', 'ig', 'inGame'])
async def check_in_game(ctx):
  if (str(ctx.author.id) == admin_key):
    await ctx.send('players in game ' + str(in_game.keys())[9:])
    
#ADMIN COMMANDS **********************************************************


@client.command()
async def say(ctx, *, repeat):
  await ctx.send(repeat)

#store deleted messages
@client.event
async def on_message_delete(message):
  message_author = str(message.author)
  
  if (not (">send" in message.content[:5])):
    
    chan2 = client.get_channel(945143392667570236) #pepe
    chan3 = client.get_channel(946986698166923295) #geng
  
    await chan2.send("AUTHOR: " + message_author + "\n" + "MESSAGE:\n" + message.content)
    await chan3.send("AUTHOR: " + message_author + "\n" + "MESSAGE:\n" + message.content)
  
  else:
    print("sent")

keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)



