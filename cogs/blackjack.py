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

        await ctx.send("This command can simulate gambling away your parent's inheritance with a game of Blackjack. Follow the instructions below to make them proud.")
        msg = await ctx.send('\nDealer:    Value: 0 \n\n' + str(ctx.author.mention)
                             + '   Value: 0     Bet: 0     Pot: ' + str(self.player_pot))
        instructions = await ctx.send("*Enter your bet. Your current winnings are $" + str(self.player_pot) + '*')
        # Main game loop
        while self.player_pot > 0:
            # Get the player's bet
            await instructions.edit(content="*Enter your bet. Your current winnings are $" + str(self.player_pot) + '*')
            bet_num = await self.client.wait_for('message', check=check)

            # Error check to see if they entered a valid bet
            if int(bet_num.content) > self.player_pot:
                await instructions.edit(content="You're too poor for that idiot. reenter the amount to bet.")
            else:
                # Subtract their bet from their pot
                self.player_pot = self.player_pot - int(bet_num.content)

                # Shuffle the deck and deal out the cards to both the bot and the player
                self.deck.shuffle(5)
                player = self.deck.deal(1)
                dealer = self.deck.deal(1)

                await msg.edit(
                    content='\nDealer:    Value: ' + str(calculate_value(dealer)) + '\n\n' + str(ctx.author.mention)
                            + '   Value: ' + str(
                        calculate_value(player)) + '     Bet: ' + bet_num.content + '    Pot: ' + str(self.player_pot))

                # Go through the player's turn
                while calculate_value(player) <= 21:
                    await instructions.edit(content='Let me know if you want to Hit or Stay. Type \'h\' to hit or \'s\' to stay.')
                    player_action = await self.client.wait_for('message', check=check)
                    # Error check the user's input
                    while player_action.content != 'h' and player_action.content != 's':
                        await instructions.edit(content="Re renter that command, can't you read? Type \'h\' to hit or \'s\' to stay.")
                        player_action = await self.client.wait_for('message', check=check)

                    # draw another card
                    if player_action.content == 'h':
                        player += self.deck.deal(1)
                        await msg.edit(content='\nDealer:    Value: ' + str(calculate_value(dealer)) + '\n\n' + str(ctx.author.mention)
                        + '   Value: ' + str(calculate_value(player)) + '     Bet: ' + bet_num.content + '    Pot: ' + str(self.player_pot))
                    # Do dealer's turn
                    elif player_action.content == 's':
                        await instructions.edit(content='Dealer\'s turn, get ready to lose!')
                        break

                if calculate_value(player) > 21:
                    await instructions.edit(content="**You lose! Goodbye inheritance!**")
                else:
                    while calculate_value(dealer) <= 21:
                        if calculate_value(dealer) < 17 and calculate_value(dealer) < calculate_value(player):
                            dealer += self.deck.deal(1)
                            await asyncio.sleep(1)
                            await msg.edit(content='\nDealer:    Value: ' + str(calculate_value(dealer)) + '\n\n' + str(
                                ctx.author.mention)
                                                   + '   Value: ' + str(
                                calculate_value(player)) + '     Bet: ' + bet_num.content + '    Pot: ' + str(
                                self.player_pot))
                        else:
                            break

                    if calculate_value(player) > calculate_value(dealer) or calculate_value(dealer) > 21:
                        await instructions.edit(content="**Dammit, you win. I'll win next time!**")
                        self.player_pot += int(bet_num.content) * 2
                    elif calculate_value(player) < calculate_value(dealer):
                        await instructions.edit(content="**You lose! Goodbye inheritance!**")
                    else:
                        await instructions.edit(content="**Wow. We just tied. This game is stupid**")
                        self.player_pot += int(bet_num.content)

                await asyncio.sleep(1)
                await instructions.edit(content="Do you want to continue? Type q to quit. Type anything else to continue")
                response = await self.client.wait_for('message', check=check)
                if response.content == 'q':
                    break


# adds the cog to the main bot
def setup(client):
    client.add_cog(BlackjackCommands(client))
