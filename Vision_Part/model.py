from typing import overload


class Deck:
    def __init__(self, is_global: bool = False):
        if is_global:
            self.deck = [4] * 13
            self.deck.append(1)
            self.deck.append(1)
        else:
            self.deck = [0] * 15
        self.played = list[list[int]]()

    def __getitem__(self, item):
        """

        :param item: rank of the card (0:A - 14:red joker) or index of the played card (-1:the last played card)
        :return: the count of the card; < 0 indicates the card has been played
        """
        if 0 <= item <= 14:
            return self.deck[item]
        elif -len(self.played) <= item < 0:
            return self.played[item]
        else:
            return None

    def __len__(self):
        """

        :return: number of cards left; < 0 indicates number of cards played
        """
        return sum(self.deck)


class Player:
    """
    Player class
    character: 0:landlord, 1:farmer, None:unset
    status: 0:playing, 1:awaiting, None:game not started
    """

    def __init__(self):
        self.deck = None
        self.character = None
        self.status = None

    def update(self, character: int):
        self.character = character
        if character == 0:
            self.status = 0
        elif character == 1:
            self.status = 1


class GameInterface:
    def __init__(self):
        pass

    def initialize(self):
        pass


class Game:
    """
    Game class
    status: 0:pre stage, 1:stage, None:game not started or game ended
    players: list of Player objects, the index indicates the position of the player(0:self, 1:next, 2:last)
    """

    def __init__(self):
        self.gi: GameInterface = GameInterface()
        self.globalDeck = Deck(is_global=True)
        self.status = None
        self.players: list[Player] = [Player() for _ in range(3)]
