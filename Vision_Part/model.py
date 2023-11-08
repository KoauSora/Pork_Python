import sys
from Vision_Part.recognize import *

game_areas = {'self_player': (0, 1 / 2, 1, 1),
              'next_player': (1 / 2, 1 / 6, 1, 1 / 2),
              'last_player': (0, 1 / 6, 1 / 2, 1 / 2),
              'public_area': (0, 0, 1, 1 / 6)}


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
        self.deck = Deck()
        self.character = None
        self.status = None


class Game:
    """
    Game class
    status: 0:pre stage, 1:stage, None:game not started or game ended
    players: list of Player objects, the index indicates the position of the player(0:self, 1:next, 2:last)
    """
    globalDeck = Deck(is_global=True)
    status = None
    players: list[Player] = [Player() for _ in range(3)]
    screen = None
    lord_position = None
