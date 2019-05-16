import discord
from discord.ext import commands
import json
import random

# The token which is used to connect to discord
TOKEN = 'NTc4Mzk5NTMzMDQ2ODI0OTcw.XN1BdQ.w-UGfZF41OmxdISeAA1VU10ZreI'

client = commands.Bot(command_prefix='~', case_insensitive=True)


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

client.run(TOKEN)
