from discord.ext import commands
import asyncio
import pydealer

# Need this for displaying the cards
suit_map = {'Diamonds': '\u2662',
            'Clubs': '\u2667',
            'Hearts': '\u2661',
            'Spades': '\u2664'}


# The cog goes here
class BlackjackCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.deck = pydealer.Deck()
        self.player_pot = 1000

    @commands.command()
    async def blackjack(self, ctx):
        # Helper function to calculate the value of a card
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

        # Helper function for editing the messages sent by the bot
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel

        # Helper function to display the cards a user has
        def hand_display(hand):
            """Returns text card display for hand
            keyword arguments:
            hand -- pydealer stack, players' hand
            """
            if not hand:
                return ''
            return_text = ''
            rank = ''
            suit = ''
            for card in hand:
                suit = suit_map[card.suit]
                if pydealer.const.DEFAULT_RANKS['values'][card.value] >= 10:
                    rank = card.value[0]
                else:
                    rank = card.value
                return_text += '| {0:2.2} {1} | '.format(rank, suit)

            return return_text

        # Helper function to show the game message
        async def game_message(string, dealer_value, dealer_hand, user, player_value, bet, player_hand):
            await string.edit(content='\nDealer:    Value: ' + dealer_value + '\n' + dealer_hand + '\n\n'+ user + '   Value: ' + player_value + '     Bet: ' + bet + '    Pot: ' + str(self.player_pot) + '\n' + player_hand)

        # Initial message sent by the bot
        msg = await ctx.send('\nDealer:    Value: 0 \n\n' + str(ctx.author.mention) + '   Value: 0     Bet: 0     Pot: ' + str(self.player_pot) + '\n')
        instructions = await ctx.send("*Enter your bet. Your current winnings are $" + str(self.player_pot) + '*')
        error = False
        # Main game loop
        while self.player_pot > 0:
            if not error:
                await instructions.edit(content="*Enter your bet. Your current winnings are $" + str(self.player_pot) + '*')
            # Get the player's bet
            bet_num = await self.client.wait_for('message', check=check)
            await ctx.channel.purge(limit=1)

            # Error check to see if they entered a valid bet
            try:
                if int(bet_num.content) > self.player_pot:
                    await instructions.edit(content="You're too poor for that idiot. reenter the amount to bet.")
                    error = True
                else:
                    # Subtract their bet from their pot
                    self.player_pot = self.player_pot - int(bet_num.content)

                    # Shuffle the deck and deal out the cards to both the bot and the player
                    self.deck.shuffle(5)
                    player = self.deck.deal(1)
                    dealer = self.deck.deal(1)

                    # Update the game's message
                    await game_message(msg, str(calculate_value(dealer)), hand_display(dealer), ctx.author.mention,
                                       str(calculate_value(player)), bet_num.content, hand_display(player))

                    # Go through the player's turn
                    while calculate_value(player) <= 21:
                        await instructions.edit(
                            content='Let me know if you want to Hit or Stay. Type \'h\' to hit or \'s\' to stay.')
                        player_action = await self.client.wait_for('message', check=check)
                        # Error check the user's input
                        while player_action.content != 'h' and player_action.content != 's':
                            await instructions.edit(
                                content="Reenter that command, can't you read? Type \'h\' to hit or \'s\' to stay.")
                            player_action = await self.client.wait_for('message', check=check)
                            await ctx.channel.purge(limit=1)

                        # draw another card
                        if player_action.content == 'h':
                            player += self.deck.deal(1)
                            await game_message(msg, str(calculate_value(dealer)), hand_display(dealer),
                                               ctx.author.mention, str(calculate_value(player)), bet_num.content,
                                               hand_display(player))
                            await ctx.channel.purge(limit=1)
                        # When choosing to stay, move to dealer's turn
                        elif player_action.content == 's':
                            await instructions.edit(content='Dealer\'s turn, get ready to lose!')
                            await ctx.channel.purge(limit=1)
                            break

                    # After the while loop ends, there is a possibility the user lost. Check if that happens.
                    if calculate_value(player) > 21:
                        await instructions.edit(content="**You lose! Goodbye inheritance!**")
                    else:
                        # Otherwise, do the dealer's turn
                        while calculate_value(dealer) <= 21:
                            if calculate_value(dealer) < 17 and calculate_value(dealer) < calculate_value(player):
                                dealer += self.deck.deal(1)
                                await asyncio.sleep(1)
                                await game_message(msg, str(calculate_value(dealer)), hand_display(dealer),
                                                   ctx.author.mention, str(calculate_value(player)), bet_num.content,
                                                   hand_display(player))
                            else:
                                break

                        # Check for win/loss here and update the pot based on the bet
                        if calculate_value(player) > calculate_value(dealer) or calculate_value(dealer) > 21:
                            await instructions.edit(content="**Dammit, you win. I'll win next time!**")
                            self.player_pot += int(bet_num.content) * 2
                        elif calculate_value(player) < calculate_value(dealer):
                            await instructions.edit(content="**You lose! Goodbye inheritance!**")
                        else:
                            await instructions.edit(content="**Wow. We just tied. This game is stupid**")
                            self.player_pot += int(bet_num.content)

                    # Check if the user wants to continue playing
                    await asyncio.sleep(2)
                    await instructions.edit(
                        content="Do you want to continue? Type q to quit. Type anything else to continue")
                    response = await self.client.wait_for('message', check=check)
                    await ctx.channel.purge(limit=1)
                    if response.content == 'q':
                        break
            except ValueError:
                error = True
                await instructions.edit(content="Enter an actual number you soggy frying pan lookin ass.")


# adds the cog to the main bot
def setup(client):
    client.add_cog(BlackjackCommands(client))
