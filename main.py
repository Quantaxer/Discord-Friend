# import statements

from discord.ext import commands

# The token which is used to connect to discord
f = open("token.txt", "r")
TOKEN = f.readline().strip()
f.close()

client = commands.Bot(command_prefix='~', case_insensitive=True)
# remove default help command to replace with custom help command

# List of file names go here for loading cogs
extensions = (
    'cogs.fun',
    'cogs.message',
    'cogs.admin',
    'cogs.reminder',
    'cogs.wiki'
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
    # default errors
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This ain't it chief (Command not found)")
    elif isinstance(error, commands.NotOwner):
        await ctx.send('Who are you? You didn\'t make me')
    # Non standard errors
    elif str(ctx.command) == "ackshually search":
        await ctx.send("Error: Missing search parameter.\nUsage: ~ackshually search (search term)")
    elif str(ctx.command) == "ackshually summary":
        await ctx.send("Error: Missing search parameter.\nUsage: ~ackshually summary (search term)")
    elif str(ctx.command) == "reminder add":
        await ctx.send("Error: Missing reminder parameter.\nUsage: ~reminder add (reminder)")
    elif str(ctx.command) == "reminder remove":
        await ctx.send("Error: Missing reminder value.\nUsage: ~reminder remove (reminder number)")
    else:
        await ctx.send(error)


@client.event
async def on_command_completion(ctx):
    await ctx.message.add_reaction(emoji='✅')


@client.command()
@commands.is_owner()
async def load(ctx, cog):
    """Loads an existing cog.\nBot owner only."""
    try:
        client.load_extension(cog)
        await ctx.send(f'Loaded `{cog}`')
    except Exception as error:
        await ctx.send(f'`{cog}` cannot be loaded. [{error}]')


@client.command()
@commands.is_owner()
async def unload(ctx, cog):
    """Unloads an existing cog.\nBot owner only."""
    try:
        client.unload_extension(cog)
        await ctx.send(f'Unloaded `{cog}`')
    except Exception as error:
        await ctx.send(f'`{cog}` cannot be unloaded. [{error}]')

# Run the client with the token
client.run(TOKEN)
