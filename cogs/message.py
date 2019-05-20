from discord.ext import commands
import discord
import asyncio


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    # event listener for any message sent
    @commands.Cog.listener()
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.client.user:
            return

        # The "I'm" commands for the dad jokes
        if 'I\'m ' in message.content:
            phrase = message.content.split('I\'m')
            msg = 'Hi' + phrase[1] + ', I\'m Dad!'.format(message)
            await message.channel.send(msg)

        if 'Im ' in message.content:
            phrase = message.content.split('Im')
            msg = 'Hi' + phrase[1] + ', I\'m Dad!'.format(message)
            await message.channel.send(msg)

        if 'im ' in message.content:
            phrase = message.content.split('im')
            msg = 'Hi' + phrase[1] + ', I\'m Dad!'.format(message)
            await message.channel.send(msg)

        if 'nice' in message.content:
            await message.channel.send("nice")

        # bruh moment
        if 'bruh' in message.content:
            await message.channel.send("This really be a bruh moment")

        # no u
        if message.content.startswith('no u'):
            await message.channel.send('no u')

        # sad waluigi noises
        if message.content.startswith('wah'):
            embed = discord.Embed()
            embed.set_image(url='https://pbs.twimg.com/profile_images/636426631876231168/8kZlHCEe_400x400.jpg')
            await message.channel.send("*sad waluigi noises*")
            asyncio.sleep(.5)
            await message.channel.send(embed=embed)


# adds the cog to the main bot
def setup(client):
    client.add_cog(Message(client))
