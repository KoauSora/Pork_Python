from Pork_Python.Vision_Part.model import *
from Pork_Python.Vision_Part.recognize import *


def updateScreen(image):
    """
    update the screen
    pyautogui is faster than imagegrab
    :return:
    """
    Game.screen = image
    pass


def initPlayers():
    """
    initialize the players after the landlord is determined
    :return:
    """
    Game.players[1].character = getPlayerCharacter(Game.screen, Game.game_areas['next_player'])
    Game.players[2].character = getPlayerCharacter(Game.screen, Game.game_areas['last_player'])

    if Game.players[1].character == 1:
        Game.players[0].character = 0
        Game.lord_position = 1
    elif Game.players[2].character == 1:
        Game.players[0].character = 0
        Game.lord_position = 2
    else:
        Game.players[0].character = 1
        Game.lord_position = 0
    Game.players[0].deck.deck = getCardsInArea(Game.screen, Game.game_areas['self_player'])


def playCards(position, played_cards=None):
    """
    play cards
    remove the cards from the deck and add them to the played list
    :param position: position of the player
    :param played_cards: if position is 0, specify the cards to play
    :return:
    """
    if played_cards is None:
        played_cards = getCardsInArea(Game.screen, Game.game_areas['last_player' if position == 2 else 'next_player'])
    Game.players[position].deck.deck = [Game.players[position].deck.deck[i] - played_cards[i] for i in range(15)]

    Game.globalDeck.deck = [Game.globalDeck.deck[i] - played_cards[i] for i in range(15)]


def getLastPlayedCards(position=None):
    """
    get the last played cards
    :param position: if position is None, get the last played cards in the global deck
    :return: the last played cards
    """
    return getCardsInArea(Game.screen, list(Game.game_areas.values())[position])


def getSelfCardPosition(rank):
    """
    get the position of the card in the self player's deck
    a list of clickable positions will be returned
    :param rank:
    :return:
    """
    return getCardPosition(Game.screen, rank)


def getHoleCards():
    """
    get the hole cards
    :return:
    """
    return getCardsInArea(Game.screen, Game.game_areas['public_area'])


def getRestCards():
    """

    :return:
    """
    return Game.globalDeck.deck


def getSelfButtonPosition(button):
    """
    get the position of the button in the self player's deck
    :param button: claim, no_claim, pass, play, no_afford, no_times
    :return:
    """
    if getButtonPosition(Game.screen, button) is None:
        return None
    else:
        return getButtonPosition(Game.screen, button)[0]
