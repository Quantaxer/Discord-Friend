from discord.ext import commands
import os
import discord


class ProductivityCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Reminder commands
    @commands.command()
    async def save_reminder(self, ctx, *, arg):
        """Saves a reminder for later reference (usage: ~save_reminder foo bar)"""
        # Get path of pun file
        cur_path = os.path.dirname(__file__)
        # Go down one directory to the parent and open file
        parent_path = os.path.split(cur_path)[0]
        new_path = os.path.relpath('data\\reminder.txt', parent_path)

        with open(new_path, 'a') as f:
            f.write("\n" + arg)
        await ctx.send("Added \"" + arg + "\" to reminders")

    @commands.command()
    async def show_reminder(self, ctx):
        """Displays all reminders that have been added"""
        # Get path of pun file
        cur_path = os.path.dirname(__file__)
        # Go down one directory to the parent and open file
        parent_path = os.path.split(cur_path)[0]
        new_path = os.path.relpath('data\\reminder.txt', parent_path)
        count = 0

        embed = discord.Embed(colour=discord.Colour.blue())
        # Create the embed
        embed.set_author(name="List of reminders")
        # Open file, read through each line and add to embed
        with open(new_path, 'r') as f:
            for line in f:
                embed.add_field(name="Reminder " + str(count), value=line, inline=False)
                count += 1

        # Send this if there are no reminders at the moment
        if count == 0:
            embed.add_field(name="No reminders set", value='\u200b', inline=False)

        await ctx.send(ctx.message.author.mention, embed=embed)

    @commands.command()
    async def clear_reminder(self, ctx):
        """Clears all reminders from the list"""
        cur_path = os.path.dirname(__file__)
        # Go down one directory to the parent and open file
        parent_path = os.path.split(cur_path)[0]
        new_path = os.path.relpath('data\\reminder.txt', parent_path)
        # Open file and clear all lines
        f = open(new_path, 'r+')
        f.truncate(0)

        await ctx.send("Cleared all contents from reminders")


# adds the cog to the main bot
def setup(client):
    client.add_cog(ProductivityCommands(client))
