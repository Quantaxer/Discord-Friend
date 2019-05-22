from discord.ext import commands
import os
import discord
import datetime


class ProductivityCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Group all commands under a certain alias
    @commands.group()
    async def reminder(self, ctx):
        """Group of commands to set reminders to view"""
        # If the user entered an invalid command go here
        if ctx.invoked_subcommand is None:
            await ctx.send("Command does not exist (add, remove, clear, display)")

    # Reminder commands
    @reminder.command()
    async def add(self, ctx, *, arg):
        """Saves a reminder for later reference (usage: ~reminder add foo bar)"""
        # Get path of pun file
        cur_path = os.path.dirname(__file__)
        # Go down one directory to the parent and open file
        parent_path = os.path.split(cur_path)[0]
        new_path = os.path.relpath('data\\reminder.txt', parent_path)

        current = datetime.datetime.now()
        with open(new_path, 'a') as f:
            f.write("Created on " + str(current.year) + "/" + str(current.month) + "/" +  str(current.day) + ": " + arg + "\n")
        await ctx.send("Added \"" + arg + "\" to reminders")

    @reminder.command()
    async def display(self, ctx):
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
                count += 1
                embed.add_field(name="Reminder " + str(count), value=line, inline=False)

        # Send this if there are no reminders at the moment
        if count == 0:
            embed.add_field(name="No reminders set", value='\u200b', inline=False)

        await ctx.send(ctx.message.author.mention, embed=embed)

    @reminder.command()
    async def clear(self, ctx):
        """Clears all reminders from the list"""
        cur_path = os.path.dirname(__file__)
        # Go down one directory to the parent and open file
        parent_path = os.path.split(cur_path)[0]
        new_path = os.path.relpath('data\\reminder.txt', parent_path)
        # Open file and clear all lines
        f = open(new_path, 'r+')
        f.truncate(0)

        await ctx.send("Cleared all contents from reminders")

    @reminder.command()
    async def remove(self, ctx, num: int):
        """Removes a selected reminder from the list (usage: ~reminder remove 2)"""
        reminders = []
        cur_path = os.path.dirname(__file__)
        # Go down one directory to the parent and open file
        parent_path = os.path.split(cur_path)[0]
        new_path = os.path.relpath('data\\reminder.txt', parent_path)
        # open file to find which reminder to remove
        with open(new_path, 'r') as f:
            for line in f:
                reminders.append(line)
        # Do error checking to see if user input was valid
        if num > len(reminders) or num <= 0:
            await ctx.send("Number not in reminders")
        else:
            # Remove the selected number and update the list
            del reminders[num - 1]
            with open(new_path, 'w') as f:
                for line in reminders:
                    f.write(line)
            await ctx.send("Removed reminder number " + str(num) + " from reminders")


# adds the cog to the main bot
def setup(client):
    client.add_cog(ProductivityCommands(client))
