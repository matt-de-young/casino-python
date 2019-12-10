""" CLI based Blackjack game """
import click

from cards import Deck, Hand


class BlackjackHand(Hand):
    """ A hand of cards for Blackjack """

    def __str__(self):
        # TODO: Dealer's hands might be rendered differently
        return f"{super(BlackjackHand, self).__str__()} : {self.value}"

    @property
    def value(self):
        """ Returns the current value of the hand """
        # TODO: Aces can be either 1 or 11
        return sum([x.rank if x.rank <= 10 else 10 for x in self.cards])

    @property
    def is_bust(self):
        """ Returns if the hand is bust or not """
        return self.value > 21


def render_table(dealer_hand, player_hand):
    """ Renders the current playing table. """
    click.clear()
    click.echo(f"Dealer: {dealer_hand}")
    click.echo(f"Player: {player_hand}")


@click.command()
def run():
    """ Starts a game of Blackjack """
    deck = Deck().shuffle()

    player_hand = BlackjackHand(deck.draw(2))
    dealer_hand = BlackjackHand(deck.draw(2))

    # TODO: Check for naturals

    # TODO: Factor gameplay loop into function so that multiple hands can be played
    while True:
        render_table(dealer_hand, player_hand)
        if click.prompt('Hit?', type=bool):
            player_hand.add(deck.draw())
            if player_hand.is_bust:
                break
        else:
            while dealer_hand.value < 17:
                dealer_hand.add(deck.draw())
                render_table(dealer_hand, player_hand)
            break

    render_table(dealer_hand, player_hand)
    if player_hand.is_bust or dealer_hand.value > player_hand.value:
        click.echo("Better luck next time!")
    elif dealer_hand.value == player_hand.value:
        click.echo("Stand-off!")
    else:
        click.echo("Winner, winner, chicken dinner!!")


if __name__ == "__main__":
    run()
