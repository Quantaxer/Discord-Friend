from discord.ext import commands
import discord
import asyncio


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command just to test if it is connected
    @commands.command()
    async def ping(self, ctx):
        """Returns time it takes to reach server"""
        await ctx.send(self.client.latency)

    # Command for the bot to yeet out of the server because why not, it's funny
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        """Leaves the server to go get smokes at the convenience store, never to return again"""
        await ctx.send("I'm just going to get some smokes from the store, I'll be back in a few minutes I swear!")
        # Find the server ID that you will leave
        to_leave = self.client.get_guild(ctx.message.guild.id)
        await to_leave.leave()

    # Plays gif of rewind time, then deletes a certain number of messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def rewind(self, ctx, amount: int):
        """It's rewind time (deletes user selected amount of messages) Amount: int > 0"""
        if amount <= 0:
            await ctx.send("You're actually stupid (amount must be > 0)")
        else:
            embed = discord.Embed()
            embed.set_image(url='https://media3.giphy.com/media/3d6WO0F9SK9hbmpsiX/giphy.gif')
            await ctx.send(embed=embed)
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=amount + 2)

    # Error handler for rewind command
    @rewind.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing required argument AMOUNT\nUsage: ~rewind 20")

    # bean command to ban a user
    @commands.command()
    async def bean(self, ctx, member: discord.Member, *, reason: str):
        """Bans a user"""
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
