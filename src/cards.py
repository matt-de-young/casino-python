""" Implementaions of playing cards """
import random
from typing import Generator, Iterable, List


class Card:
    """ Standard playing card """
    def __init__(self, suit: str, rank: int) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        if self.rank == 11:
            return f"[J{self.suit}]"
        if self.rank == 12:
            return f"[Q{self.suit}]"
        if self.rank == 13:
            return f"[K{self.suit}]"
        if self.rank == 1:
            return f"[A{self.suit}]"

        return f"[{self.rank}{self.suit}]"


class Deck:
    """ Standard 52 card deck """
    def __init__(self) -> None:
        self.cards: List[Card] = [
            Card(suit, rank) for suit in ["♣", "♦", "♥", "♠"] for rank in range(1, 14)
        ]


    def shuffle(self) -> "Deck":
        """ Shuffles the cards in the deck """
        for i in range(len(self.cards)):
            x = random.randint(0, i)
            self.cards[i], self.cards[x] = self.cards[x], self.cards[i]
        return self

    def draw(self, n: int = 1) -> Generator[Card, None, None]:
        """ Pops one card from the deck """
        yield from [self.cards.pop() for _ in range(n)]


class Hand:
    """ A hand of cards """
    def __init__(self, cards: Iterable[Card] = None) -> None:
        self.cards = list(cards) if cards else []

    def __str__(self) -> str:
        return " ".join(str(card) for card in self.cards)

    def __bool__(self) -> bool:
        return bool(self.cards)

    def add(self, cards: Iterable[Card]) -> None:
        """ Adds a card or cards to the hand """
        self.cards.extend(list(cards))
