from discord.ext import commands
import discord
import asyncio


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # custom help command
    @commands.command()
    async def help(self, ctx):
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Colour.blue())
        # Create the embed
        embed.set_author(name="List of commands")
        embed.add_field(name="~b", value="fills a sentence with the b emoji. Must have at least one word following command",
                        inline=False)
        embed.add_field(name="~bean", value="Bans a user", inline=False)
        embed.add_field(name="~bedtime", value="Tells you to go to sleep", inline=False)
        embed.add_field(name="~colossal", value="Creates a colossal mess in chat. Not for the faint of heart", inline=False)
        embed.add_field(name="~funky", value="Funky consoles you in your time of need", inline=False)
        embed.add_field(name="~leave",
                        value="Leaves the server to go get smokes at the convenience store, never to return again",
                        inline=False)
        embed.add_field(name="~ping", value="returns time it takes to reach server", inline=False)
        embed.add_field(name="~pointer", value="A terrible explanation of how a pointer works in c", inline=False)
        embed.add_field(name="~pun", value="Tells a random dad joke that nobody likes", inline=False)
        embed.add_field(name="~rewind", value="It's rewind time (deletes user selected amount of messages)", inline=False)

        # send the embed
        await ctx.send(author.mention, embed=embed)

    # Plays gif of rewind time, then deletes a certain number of messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def rewind(self, ctx, amount: int):
        embed = discord.Embed()
        embed.set_image(url='https://media3.giphy.com/media/3d6WO0F9SK9hbmpsiX/giphy.gif')
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=amount + 2)

    # Error handler for rewind command
    @rewind.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing required argument AMOUNT\nUsage: ~rewind 20")

    # bean command to ban a user
    @commands.command()
    async def bean(self, ctx, member: discord.Member, *, reason: str):
        # Send bean message
        await ctx.send(f'Lmao you were beaned by {ctx.author.display_name} because you were {reason}!')

        # Show image of bean
        embed = discord.Embed()
        embed.set_image(
            url='https://i1.sndcdn.com/artworks-000192834342-vjqze6-t500x500.jpg')
        await ctx.send(embed=embed)

        # Wait and then ban the user
        await asyncio.sleep(2)
        await member.ban(reason=reason)

    # error handler for bean command
    @bean.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing required argument\n Usage: ~bean @user \"reason\"")

# adds the cog to the main bot
def setup(client):
    client.add_cog(AdminCommands(client))
