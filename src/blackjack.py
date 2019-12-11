""" CLI based Blackjack game """
from typing import Any, Optional

import click

from cards import Card, Deck, Hand


PLAYER_BANK: int

class BlackjackHand(Hand):
    """ A hand of cards for Blackjack """

    def __str__(self) -> str:
        return f"{super(BlackjackHand, self).__str__()} : {self.value if self.value <= 21 else 'bust'}"

    def render(self, reveal: bool = False) -> str:
        """ Represents the hand as a string including face down cards by default """
        if reveal:
            return self.__str__()
        else:
            return "[??] " + " ".join(str(card) for card in self.cards[1:])

    @property
    def _raw_value(self) -> int:
        """ Returns the value of hand, counting aces as 11 """
        card_values = {
            1: 11,
            **{i: i for i in range(2, 10)},
            **{i: 10 for i in range(10, 14)},
        }
        return sum([card_values[x.rank] for x in self.cards])


    @property
    def value(self) -> int:
        """ Returns the current value of the hand """
        if not any(x.rank == 1 for x in self.cards) or self._raw_value <= 21:
            return self._raw_value

        # Aces can be either 1 or 11
        soft_value: int = self._raw_value
        for _ in range(sum([1 if x.rank == 1 else 0 for x in self.cards])):
            soft_value -= 10
            if soft_value <= 21:
                break

        return soft_value

    @property
    def is_bust(self) -> bool:
        """ Returns if the hand is bust or not """
        return self.value > 21

    @property
    def is_soft(self) -> bool:
        """ Returns if the hand is could possibly be a lower value or not """
        return sum([x.rank if x.rank < 9 else 10 for x in self.cards]) == self.value


def render_table(
        dealer_hand: BlackjackHand,
        player_hand: BlackjackHand,
        reveal_dealer: bool = False
    ) -> None:
    """ Renders the current playing table. """
    click.clear()
    click.echo(f"Dealer: {dealer_hand.render(reveal=reveal_dealer)}")
    click.echo(f"Player: {player_hand.render(reveal=True)}")
    click.echo("")


def play_hand(bet: int) -> int:
    """ Play a single hand of Blackjack """
    deck = Deck().shuffle()

    player_hand = BlackjackHand(deck.draw(2))
    dealer_hand = BlackjackHand(deck.draw(2))

    # Check for blackjack
    if player_hand.value == 21 and dealer_hand.value == 21:
        click.echo("Stand-off.")
        return bet
    elif dealer_hand.value == 21:
        click.echo("Dealer Blackjack.")
        return 0
    elif player_hand.value == 21:
        click.echo("Blackjack!")
        return int(bet * 1.5)

    while True:
        render_table(dealer_hand, player_hand)
        if click.prompt("Hit?", type=bool):
            player_hand.add(deck.draw())
            if player_hand.is_bust:
                break
        else:
            while dealer_hand.value < 17 and not dealer_hand.is_soft:
                dealer_hand.add(deck.draw())
                render_table(dealer_hand, player_hand)
            break

    render_table(dealer_hand, player_hand, reveal_dealer=True)
    if player_hand.is_bust or (dealer_hand.value > player_hand.value and not dealer_hand.is_bust):
        click.echo("Better luck next time.")
        return 0
    elif dealer_hand.value == player_hand.value:
        click.echo("Stand-off.")
        return bet
    else:
        click.echo("Winner, winner, chicken dinner!!")
        return bet * 2


def validate_bet(value: Any) -> Optional[int]:
    """ Validates bet input to make sure it's valid """
    global PLAYER_BANK
    try:
        if int(value) >= PLAYER_BANK:
            raise click.BadParameter(f"You don't have enough money to bet ${value}", param=value)
        else:
            return int(value)
    except ValueError:
        raise click.BadParameter("Not a valid bet.", param=value)
    # return value


@click.command()
def run() -> None:
    """ Starts a game of Blackjack """
    global PLAYER_BANK

    PLAYER_BANK = 100
    bet = click.prompt(
        f"Starting a new game with ${PLAYER_BANK}. What would you to bet?",
        value_proc=validate_bet,
        prompt_suffix=" $"
    )

    while True:
        PLAYER_BANK -= bet
        PLAYER_BANK += play_hand(bet)

        click.echo(f"Bank: ${PLAYER_BANK}")
        if PLAYER_BANK <= 0:
            click.echo(f"Game over.")
            break

        bet = click.prompt(
            f"Change your bet?",
            value_proc=validate_bet,
            prompt_suffix=" $",
            default=bet
        )


if __name__ == "__main__":
    run()
