from discord.ext import commands
import praw
import asyncio
import random


class RedditCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Retrieve the information required to connect to the reddit API. Kept separate from code for security
        # You can get this same information by creating a reddit app at https://www.reddit.com/prefs/apps. user agent is simply a string with your username in it.
        f = open("praw.txt", "r")
        arr = f.readlines()
        f.close()
        # Create the reddit class using the info retrieved from the text file
        self.reddit = praw.Reddit(client_id=arr[0].strip(),
                                  client_secret=arr[1].strip(),
                                  user_agent=arr[2].strip())

    @commands.command()
    async def pupper(self, ctx):
        """Fills the chat with cute pictures of doggos, choosing the hot pictures from a random subreddit"""
        # subreddit list is here
        subreddit_list = ['rarepuppers', 'puppies', 'shiba', 'goldenretrievers', 'WhatsWrongWithYourDog']
        submissions = self.reddit.subreddit(subreddit_list[random.randint(0, 4)]).hot(limit=8)
        for post in submissions:
            # Ignore stickied posts since they are usually just user information/ rules
            if not post.stickied:
                # send the url in chat
                await ctx.send(post.url)
                await asyncio.sleep(1)

    # Group all commands under a certain alias
    @commands.group()
    async def reddit(self, ctx):
        """Group of commands for subreddits"""
        # If the user entered an invalid command go here
        if ctx.invoked_subcommand is None:
            await ctx.send("Command does not exist (search)")

    @reddit.command()
    async def search(self, ctx, *, arg):
        """User can search for a subreddit and retrieve information about it"""
        try:
            the_sub = self.reddit.subreddit(arg)
            await ctx.send(the_sub.public_description)
        except:
            await ctx.send("Sorry, that subreddit couldn't be accessed. It either does not exist or is misspelled")


# adds the cog to the main bot
def setup(client):
    client.add_cog(RedditCommands(client))
