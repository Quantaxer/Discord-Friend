from discord.ext import commands


class MessageCog(commands.Cog):
    def __init__(self, client):
        self.client = client

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

        # THIS IS STUPID for some reason you need this line here for commands to work
        await self.client.process_commands(message)

# adds the cog to the main bot
def setup(client):
    client.add_cog(MessageCog(client))
