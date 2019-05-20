# import statements

from discord.ext import commands

# The token which is used to connect to discord
f = open("token.txt", "r")
TOKEN = f.readline().strip()
f.close()

client = commands.Bot(command_prefix='~', case_insensitive=True)
# remove default help command to replace with custom help command
client.remove_command('help')

# List of file names go here for loading cogs
extensions = (
    'cogs.fun',
    'cogs.message',
    'cogs.admin'
)

# Loops through extensions list and loads each cog
if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(extension)


# Shows we are connected and running
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Default error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This ain't it chief (Command not found)")

# Run the client with the token
client.run(TOKEN)
