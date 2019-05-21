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
        """Searches Wikipedia for any related pages"""
        data = wikipedia.search(arg)
        await ctx.send("These are all the pages I found about " + arg + ":")
        msg = "\n".join(data)
        await ctx.send(msg)

    @wiki.command()
    async def summary(self, ctx, *, arg):
        """Provides a brief 5 sentence summary for a certain Wikipedia page"""
        try:
            msg = "**This is what I found:**\n\n" + wikipedia.summary(arg, sentences=5)
        except wikipedia.exceptions.DisambiguationError as e:
            # occurs when the result is a disambiguation page
            size = len(e.options)
            # only display 10 options if more exist
            if size > 9:
                msg = "**This is a disambiguation page. Here are some related pages instead.**\n\n" + '\n'.join(e.options[0:9]) + "\n*And " + str(size - 10) + " more*"
            else:
                msg = "**This is a disambiguation page. Here are some related pages instead.**\n\n" + '\n'.join(e.options)
        except wikipedia.exceptions.PageError as e:
            # occurs if the page doesn't exist
            msg = e

        await ctx.send(msg)


# adds the cog to the main bot
def setup(client):
    client.add_cog(WikiCommands(client))
