from discord.ext import commands
import discord
import os
import random
import datetime
import asyncio


class CommandCogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command just to test if it is connected
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(self.client.latency)

    # Command for the bot to yeet out of the server because why not, it's funny
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        await ctx.send("I'm just going to get some smokes from the store, I'll be back in a few minutes I swear!")
        # Find the server ID that you will leave
        to_leave = self.client.get_guild(ctx.message.guild.id)
        await to_leave.leave()

    # Bedtime command, because everyone should go to sleep at 7 pm like civilized people
    @commands.command()
    async def bedtime(self, ctx):
        current = datetime.datetime.now().time()
        if ((current.hour >= 19) or (current.hour < 6)) and (current.minute > 0):
            await ctx.send("You should really go to sleep, You are past your bedtime of 7:00 pm")
        elif ((current.hour >= 0) and (current.hour < 6)) and (current.minute > 0):
            await ctx.send("Boi it's past midnight you have school tomorrow, Mrs. Jablinski will slap you silly!")
        else:
            await ctx.send("It is not 7:00 pm yet, keep on doing what you're doing!")

    # puns command, reads puns fro ma file and selects one at random
    @commands.command()
    async def pun(self, ctx):
        list_of_puns = []
        # Get path of pun file
        cur_path = os.path.dirname(__file__)
        new_path = os.path.relpath('..\\data\\puns.txt', cur_path)
        # open file and append each line to the list
        with open(new_path, 'r') as f:
            for line in f:
                list_of_puns.append(line)

        # select a random pun and print it
        i = random.randint(0, 39)
        await ctx.send(list_of_puns[i])

    # colossal command, injects a bunch of garbage into the channel it was called in
    @commands.command()
    async def colossal(self, ctx):
        trash = ["the bruh momentum is the event leading up to a bruh moment",
                 "hf hf hf hf hf hf hf hf\nhf hf hf hf hf hf hf hf",
                 "anyways, {} is getting their ass exposed".format(ctx.author.mention),
                 "dedotated W A M",
                 "Help my pee is orange I'm rotting",
                 "Meet marcel toing. Proud owner of restaurant ratatatatoing\nchef toing toing.\nserving only the freshest toing.",
                 "seeya idot",
                 "THAT'S IT, I\'M GONNA DDOS YOU",
                 "mmmmm c r e a m y",
                 "snans",
                 "SNANS",
                 "MINECRAP",
                 "Ok yeah sure thing that's valid whatever you say Mr. Galaxy Brain you're the real colossal mess",
                 "wan go diney wurl\nflawda?\northano\nme wanna go flawda\ndindlee whirld!",
                 "This is an absolute colossal mess",
                 "Don't mind me I'm just a bit of a mess",
                 "My treehouse, my rules. No trees allowed",
                 "SQUILLIAMS TENNISBALLS",
                 "Is it CRONCH time?\nIt is always spicy big C R O N C H time",
                 "I have my pocket right here in my pocket"]

        # loop and choose a random t r a s h to print
        for i in range(40):
            await ctx.send(trash[random.randint(0, 19)])
            await asyncio.sleep(1.5)

    # Command to 🅱ify a sentence
    @commands.command(pass_context=True)
    async def b(self, ctx, *args):
        new_list = []
        # check if command was used properly
        if len(args) == 0:
            await ctx.send("Include at least one word in that command you garfield lookin ass")
        # loop through arguments
        for i in args:
            # edit the string, replacing b with emoji B. Also need to set string to lowercase
            new_str = i.lower().replace('b', '🅱')
            # Create a temp list in order to edit the first character because python strings are immutable
            temp_list = list(new_str)
            temp_list[0] = '🅱'
            final_str = "".join(temp_list)
            # append final version of the word
            new_list.append(final_str)

        await ctx.send(" ".join(new_list))

    # A terrible explanation of what a pointer is
    @commands.command()
    async def pointer(self, ctx):
        await ctx.send("A pointer is something that points to a point in memory. This point is where the pointer is stored, allowing you to do stuff. You can even have pointers that point to pointers, which is called a double pointer. For example, you could have a pointer point to a pointer that points to a structure that has a variable which is a pointer to a pointer to an integer. There is no point.\n-Professor Kremer, phd in bigbrain")

    # funky kong command
    @commands.command()
    async def funky(self, ctx):
        await ctx.send("Funky cares for all your needs. Funky loves you for who you are.")
        await asyncio.sleep(1.5)
        await ctx.send("https://www.youtube.com/watch?v=68JQtxTzjqc")
        await asyncio.sleep(1.5)
        await ctx.send("https://www.youtube.com/watch?v=Dj7K2Bql6D4")
        await asyncio.sleep(1.5)
        embed = discord.Embed()
        embed.set_image(url='https://vignette.wikia.nocookie.net/mario/images/b/b0/Funky_Kong_Artwork_-_Mario_Kart_Wii.png/revision/latest?cb=20120424225007')
        await ctx.send(embed=embed)


# adds the cog to the main bot
def setup(client):
    client.add_cog(CommandCogs(client))
