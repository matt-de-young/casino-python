""" Implementaions of playing cards """
import random


class Card:
    """ Standard playing card """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self.rank == 11:
            return f"[J{self.suit}]"
        if self.rank == 12:
            return f"[Q{self.suit}]"
        if self.rank == 13:
            return f"[K{self.suit}]"
        if self.rank == 14:
            return f"[A{self.suit}]"

        return f"[{self.rank}{self.suit}]"


class Deck:
    """ Standard 52 card deck """
    def __init__(self):
        self.cards = []
        for suit in ["♣", "♦", "♥", "♠"]:
            for val in range(1, 14):
                self.cards.append(Card(suit, val))

    def shuffle(self):
        """ Shuffles the cards in the deck """
        for i in range(len(self.cards) - 1, 0, -1):
            x = random.randint(0, i)
            self.cards[i], self.cards[x] = self.cards[x], self.cards[i]
        return self

    def draw(self, n=1):
        """ Pops one card from the deck """
        yield from [self.cards.pop() for _ in range(n)]

class Hand:
    """ A hand of cards """
    def __init__(self, cards=None):
        self.cards = list(cards) if cards else []

    def __str__(self):
        return " ".join(str(card) for card in self.cards)

    def __bool__(self):
        return bool(self.cards)

    def add(self, card):
        """ Adds a card or cards to the hand """
        self.cards.extend(list(card))
