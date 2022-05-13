import discord
import os   #neded for taking the token 
from keep_alive import keep_alive   #needed for keeping the bot alive (pings the bot)
from discord.ext import commands
import random
import copy
import Profile

roster = {} #people with profiles

client = commands.Bot(command_prefix = '<')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online,     activity=discord.Game("creator: Light"))
  print('ASTRO_BOT STATUS: ONLINE')

#Custom reponses to different users
@client.command(aliases=['hello', 'Hello', 'HELLO'])
async def hi(ctx):
  message_author = str(ctx.author)
  if (message_author == "Light#5080"):
    await ctx.send("Sir! :smile:")
  #add custom responses here--

#initialize inbox
@client.command(aliases= ['mkbox', 'new'])
async def _mkinbox(ctx):
  author = str(ctx.author)
  if (not (author in roster)):
    roster[author] = Profile.Profile(author)
  else:
    await ctx.send("Inbox already exist")

#how many messages
@client.command(aliases= ['box', 'inbox'])
async def _inbox(ctx):
  author = str(ctx.author)
  if (author in roster):
    messages = str(len(roster[author].get_inbox()))
    await ctx.send(messages + " message(s)")
  else:
    await ctx.send("Inbox does not exist")
    
#send messages
@client.command(aliases= ['send', 's'])
async def _send(ctx, *, message):
  author = message.split(' ', 1)[0]
  if (author in roster):
    roster[author].add_message(message.split(' ', 1)[1])
  await ctx.message.delete()
  
#read messages
@client.command(aliases= ['read', 'r'])
async def _open(ctx):
  author = str(ctx.author)
  if (author in roster) and (len(roster[author].get_inbox()) != 0):
    message = str(roster[author].read_message())
    await ctx.send("anonymous: " + message)
  else:
    await ctx.send("No message(s) available")

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
in_game = {} #players in game
queue = [] #invites sent
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

#Find if player is in the roster, if true then return player's game key, else return empty string
def find_key(player):
  if not (player in roster):
    return ""
  return roster[player].get_gameKey()

def get_other_player(key, player):
  player2 = key.replace(player, "")
  player2 = player2.strip()
  return player2

def reset_players(key, player):
  player2 = get_other_player(key, player)
  roster[player].reset_myTurn()
  roster[player2].reset_myTurn()

#Finds the appropriate index for the position on the board to be filled in ('X' or 'O')
def find_index(spot):
  if ((spot >= 1) & (spot <= 3)):
    pos = (0, (spot - 1))
  elif ((spot >= 4) & (spot <= 6)):
    pos = (1, (spot - 4))
  elif ((spot >= 7) & (spot <= 9)):
    pos = (2, (spot - 7))
  else:
    pos = 0
  return pos

@client.command(aliases=['t'])
async def TTT(ctx):
  author = str(ctx.author)
  key = roster[author].get_gameKey()
  await ctx.send(printB(key))

#Player makes a move
@client.command(aliases=['tic', 'tac', 'toe'])
async def turn(ctx, spot):
  spot = (int(spot))
  player = str(ctx.author)
  win_condition = False
  tie_condition = False
  key = find_key(player)
  
  pos = find_index(spot)
  if not pos:
    await ctx.send('Invalid spot!')
    #return False

  if (roster[player].get_myTurn()):
    if (in_game[key][pos[0]][pos[1]] != 'O') & (in_game[key][pos[0]][pos[1]] != 'X'):
      if (player in str(key)):
        if (in_game[key][3] % 2 == 0):          #even, 0,2,4... (checks the number of turns)
          in_game[key][pos[0]][pos[1]] = 'O'
          win_condition = check_winner(pos, 'O', key)
        else:                                   #odd, 1,3,5... (checks the number of turns)
          in_game[key][pos[0]][pos[1]] = 'X'
          win_condition = check_winner(pos, 'X', key)
        in_game[key][3] += 1 #incriment total number of turns
        if (not win_condition):
          tie_condition = check_tie(key)
      else:
        await ctx.send('You are not registered in a game!')
        #return False
    else:
      await ctx.send('Invalid spot!')
      #return False
  else:
    await ctx.send('Not your turn!')
    #return False

  #Update myTurn field for each player
  if (in_game[key][3] > 1):
    player2 = get_other_player(key, player)
    roster[player2].set_myTurn()
  roster[player].set_myTurn()

  await ctx.send("---" + key + "---")
  if win_condition:
    await ctx.send(printB(key))
    await ctx.send('Total Moves: ' + str(in_game[key][3]))
    await ctx.send(str(ctx.author) + 'Wins!')
    reset_players(key, player)
    in_game.pop(key)
  elif (tie_condition):
    await ctx.send(printB(key))
    await ctx.send('Total Moves: ' + str(in_game[key][3]))
    await ctx.send(str('Thats a tie!'))
    reset_players(key, player)
    in_game.pop(key)
  else:
    await ctx.send(printB(key))
    await ctx.send('Total Moves: ' + str(in_game[key][3]))

#Check for win condition----------------------------------------------------------
def check_winner(pos, letter, key):
  board = in_game[key]
  row = check_row(pos, letter, board)
  col = check_col(pos, letter, board)
  diag = check_diagonal(pos, letter, board)
  if (row or col or diag):
    return True
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

  if ((pos[0] == 0) & (pos[1] == 0)) | ((pos[0] == 2) & (pos[1] == 2)):
    for i in range (len(diagonal1)):
      if diagonal1[i] != letter:
        return False
  else:
    for j in range (len(diagonal2)):
      if diagonal2[j] != letter:
        return False
  return True

#Check for Tie
def check_tie(key):
  board = in_game[key]
  for i in range(len(board[0])):
    for j in range(len(board) - 1):
      if ((board[i][j] != 'X') and (board[i][j] != 'O')):
        return False
  return True
        
#--------------------------------------------------------------------------------------------
#INVITING AND ACCEPTING------------------------------------------------------------
#INVITE
@client.command(aliases = ['i', 'inv', 'invite'])
async def send_invite(ctx, invite):
  author = str(ctx.author)
  key = author + " " + str(invite)
  if (author in roster) and (str(invite) in roster):
    if (not(key in queue)):
      queue.append(key)
    else:
      await ctx.send("already sent an invite to " + invite)
  else:
    await ctx.send("```Error! Either you or the person you are trying to invite does not have a profile!\nPlease create a profile by typing the command '<new'```")

#ACCEPT 
@client.command(aliases = ['k', 'okey', 'accept'])
async def _accept(ctx, host):
  author = str(ctx.author)
  key = str(host) + " " + author
  if (key in queue):
    queue.remove(key)
    roster[author].set_gameKey(key)
    roster[str(host)].set_gameKey(key)
    in_game[key] = copy.deepcopy(x)
    #await ctx.send('KEY: ' + key)
    await ctx.send(printB(key))
  else:
    await ctx.send(host + " has not given you an invite")

#DECLINE 
@client.command(aliases = ['n', 'no', 'decline'])
async def _decline(ctx, host):
  author = str(ctx.author)
  key = str(host) + " " + author
  if (key in queue):
    queue.remove(key)
  else:
    await ctx.send(host + " has not given you an invite")
#-------------------------------------------------------------------------------------------
#Tic Tac Toe Game END HERE ----

@client.command(aliases = ['commands', 'com', 'c'])
async def _help(ctx):
  commands = ('```COMMANDS:' + "\n" +
"<mkbox => create your inbox. (people will be able to send messages to you anonymously." + "\n" +
"<send (userID#1234) (message here) => send message to userID#1234. Receiver will not know the sender." + "\n" +
"<box => display how many messages are in your inbox." + "\n" +
"<read => open message from inbox one at a time (from most recent to oldest)." + "\n" +
"<invite (userID#1234) => invite userID#1234 to play TicTacToe (for now, will add more games in future updates)." + "\n" +
"<accept => accept userID#1234's TicTacToe invitation. The TicTacToe board will be displayed along with the KEY." + "\n" +
"<tic (KEY) (position number) => places 'X' or 'O' on the board according to the position number given." + "\n" +
"NOTE: The KEY is used to differentiate you from other players who are also playing TicTacToe. In other words," + "\n" +
"     multiple people should be able to play TicTacToe simultaneously." + "\n" + 
"Next Updates:" + "\n" +
"- Possibly improve TicTacToe so that only one person at a time can make moves." + "\n" +
"- Add Scoring System (may take a while)" + "\n" +
"- Add Hangman game (may take a while)" + "\n" +
"- Add Guess the number game (not a priority thus may take a while)" + "\n" +
"- Add a status profile (may be added along scoring system)" + "\n" +
"- Add fortune cookie system. Winning games may reward you a fortune cookie. Opening a fortune cookie will tell" + "\n" +
"  you a fortune. (may be added along scoring system)" + "\n" +
"- Bug: sometimes messages from inbox will disapear in about 5hr after it is sent. (may take a while to fix)```")
  await ctx.send(commands)

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
    await ctx.send('players in queue: ' + str(queue))

#check current in_game
@client.command(aliases= ['ingame', 'ig', 'inGame'])
async def check_in_game(ctx):
  if (str(ctx.author.id) == admin_key):
    await ctx.send('players in game: ' + str(in_game.keys())[9:])
    
#ADMIN COMMANDS **********************************************************

@client.command()
async def say(ctx, *, repeat):
  await ctx.send(repeat)

#store deleted messages (send deleted messages to certain text channel(s))
@client.event
async def on_message_delete(message):
  message_author = str(message.author)

  if ((message_author == "Pancake#3691") | (message_author == "Astro Bot#1484")):
    print('bot')
  elif  (not (("<send" in message.content.split(' ', 1)[0]) | ('<s' in message.content.split(' ', 1)[0]))):
    chan2 = client.get_channel(945143392667570236) #pepe
    chan3 = client.get_channel(946986698166923295) #squad
  
    await chan2.send("AUTHOR: " + message_author + "\n" + "MESSAGE:\n" + message.content)
    await chan3.send("AUTHOR: " + message_author + "\n" + "MESSAGE:\n" + message.content)
  else:
    print("sent")

keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)