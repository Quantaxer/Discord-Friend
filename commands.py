# import statements
import datetime
from discord.ext import commands
import os
import random

# The token which is used to connect to discord
TOKEN = 'NTc4Mzk5NTMzMDQ2ODI0OTcw.XN1BdQ.w-UGfZF41OmxdISeAA1VU10ZreI'
client = commands.Bot(command_prefix='~', case_insensitive=True)

# Shows we are connected and running
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# This garbage ain't working, maybe need to split commands and events
"""@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # The "I'm" commands for the dad jokes
    if 'I\'m' in message.content:
        phrase = message.content.split('I\'m')
        msg = 'Hi' + phrase[1] + ', I\'m Dad!'.format(message)
        await message.channel.send(msg)

    if 'Im' in message.content:
        phrase = message.content.split('Im')
        msg = 'Hi' + phrase[1] + ', I\'m Dad!'.format(message)
        await message.channel.send(msg)

    if 'im' in message.content:
        phrase = message.content.split('im')
        msg = 'Hi' + phrase[1] + ', I\'m Dad!'.format(message)
        await message.channel.send(msg)
"""

# Command just to test if it is connected
@client.command()
async def ping(ctx):
    await ctx.send(client.latency)

# Command for the bot to yeet out of the server because why not, it's funny
@client.command(pass_context=True)
async def leave(ctx):
    await ctx.send("I'm just going to get some smokes from the store, I'll be back in a few minutes I swear!")
    # Find the server ID that you will leave
    to_leave = client.get_guild(ctx.message.guild.id)
    await to_leave.leave()

# Bedtime command, because everyone should go to sleep at 7 pm like civilized people
@client.command()
async def bedtime(ctx):
    current = datetime.datetime.now().time()
    if ((current.hour >= 19) or (current.hour < 6)) and (current.minute > 0):
        await ctx.send("You should really go to sleep, You are past your bedtime of 7:00 pm")
    elif ((current.hour >= 0) and (current.hour < 6)) and (current.minute > 0):
        await ctx.send("Boi it's past midnight you have school tomorrow, don't want Mrs. Jablinski to slap you")
    else:
        await ctx.send("It is not 7:00 pm yet, keep on doing what you're doing!")

# puns command, reads puns fro ma file and selects one at random
@client.command()
async def pun(ctx):
    list_of_puns = []
    # Get path of pun file
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('data\\puns.txt', cur_path)
    # open file and append each line to the list
    with open(new_path, 'r') as f:
        for line in f:
            list_of_puns.append(line)

    # select a random pun and print it
    i = random.randint(0, 39)
    await ctx.send(list_of_puns[i])

client.run(TOKEN)
