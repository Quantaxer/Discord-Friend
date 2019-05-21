from discord.ext import commands
import wikipedia


class WikiCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Group all commands under a certain alias
    @commands.group()
    async def wiki(self, ctx):
        # If the user entered an invalid command go here
        if ctx.invoked_subcommand is None:
            await ctx.send("Command does not exist ()")

    @wiki.command()
    async def search(self, ctx, *, arg):
        """Searches wikipedia for any related pages"""
        data = wikipedia.search(arg)
        await ctx.send("These are all the pages I found about " + arg + ":")
        msg = "\n".join(data)
        await ctx.send(msg)


# adds the cog to the main bot
def setup(client):
    client.add_cog(WikiCommands(client))