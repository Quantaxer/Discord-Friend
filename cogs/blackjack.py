from discord.ext import commands
import discord
import asyncio
import pydealer


class BlackjackCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.deck = pydealer.Deck()
        self.player_pot = 1000

    @commands.command()
    async def blackjack(self, ctx):

        def calculate_value(card_hand):
            """Calculates value of player's hand"""
            if not card_hand:
                return 0
            num_aces = 0
            total_value = 0
            for card in card_hand:
                if pydealer.const.DEFAULT_RANKS['values'][card.value] == 13:
                    num_aces += 1
                    total_value += 11
                elif pydealer.const.DEFAULT_RANKS['values'][card.value] >= 10:
                    total_value += 10
                else:
                    total_value += int(card.value)

            while num_aces > 0 and total_value > 21:
                total_value -= 10
                num_aces -= 1

            return total_value

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel

        # Main game loop
        while True:
            # Get the player's bet
            await ctx.send("Enter your bet. Your current winnings are $" + str(self.player_pot))
            bet_num = await self.client.wait_for('message', check=check)

            # Error check to see if they entered a valid bet
            if int(bet_num.content) > self.player_pot:
                await ctx.send("You're too poor for that idiot")
            else:
                # Subtract their bet from their pot
                self.player_pot = self.player_pot - int(bet_num.content)

                # Shuffle the deck and deal out the cards to both the bot and the player
                self.deck.shuffle(5)
                player = self.deck.deal(1)
                dealer = self.deck.deal(1)

                # Go through the player's turn
                while calculate_value(player) <= 21:
                    await ctx.send("hehe" + str(calculate_value(player)))

                    player_action = await self.client.wait_for('message', check=check)
                    # Error check the user's input
                    while player_action.content != 'h' and player_action.content != 's':
                        await ctx.send("Re renter that command, can't you read?")
                        player_action = await self.client.wait_for('message', check=check)

                    # draw another card
                    if player_action.content == 'h':
                        player += self.deck.deal(1)
                    # Do dealer's turn
                    elif player_action.content == 's':
                        break

                if calculate_value(player) > 21:
                    await ctx.send("You lose!")
                else:
                    while calculate_value(dealer) <= 21:
                        if calculate_value(dealer) < 17:
                            dealer += self.deck.deal(1)
                        else:
                            break

                    await ctx.send(calculate_value(dealer))
                    if calculate_value(player) > calculate_value(dealer) or calculate_value(dealer) > 21:
                        await ctx.send("You win!")
                        self.player_pot += int(bet_num.content) * 2
                    elif calculate_value(player) < calculate_value(dealer):
                        await ctx.send("You lose!")
                    else:
                        await ctx.send("Tie!")
                        self.player_pot += int(bet_num.content)

                await ctx.send("Do you want to continue? Type q to quit. Type anything else to continue")
                response = await self.client.wait_for('message', check=check)
                if response.content == 'q':
                    break

                await ctx.send(player)


# adds the cog to the main bot
def setup(client):
    client.add_cog(BlackjackCommands(client))
