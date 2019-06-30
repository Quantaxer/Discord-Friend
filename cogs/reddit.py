from discord.ext import commands
import praw


class RedditCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        f = open("praw.txt", "r")
        arr = f.readlines()
        f.close()
        self.reddit = praw.Reddit(client_id=arr[0].strip(),
                                  client_secret=arr[1].strip(),
                                  user_agent=arr[2].strip())

    @commands.command()
    async def pupper(self, ctx):
        print(self.reddit.read_only)


# adds the cog to the main bot
def setup(client):
    client.add_cog(RedditCommands(client))
