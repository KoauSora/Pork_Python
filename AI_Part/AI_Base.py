import torch
from Vision_Part.model import *


class Play_Test:
    def __init__(self):
        self.global_deck = Deck()
        self.landlord_deck = Deck()
        self.next_deck = Deck()
        self.last_deck = Deck()
        self.goal_deck = Deck()
        self.character = None
        self.situation = None

    def get_deck(self):
        return self.goal_deck

    def need_Game(self):
        self.global_deck = Game.globalDeck
        self.character = Game.players[0]

    def need_other_deck(self):
        pass

    def run(self):
        pass