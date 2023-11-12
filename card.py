from enum_suit import Suit

class Card:
    suit: Suit
    value: int
    agent: "Agent"

    def __init__(self, suit: Suit, value: int):
        self.suit = suit
        self.value = value

    def get_numerical_value(self) -> int: 
        return self.suit.value * 13 + self.value

