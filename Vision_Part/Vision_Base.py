from abc import ABC, abstractmethod
from model import *


class VisionVirtualBase(ABC):
    @abstractmethod
    def getGameStatus(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def getPlayerCharacter(self, position):
        """

        :return:
        """
        pass

    @abstractmethod
    def getPlayerDeck(self, position) -> Deck:
        """

        :return:
        """
        pass

    @abstractmethod
    def getRestCard(self) -> list[int]:
        """

        :return:
        """
        pass

    @abstractmethod
    def getSelfPlayerStatus(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def getSelfCardsPositions(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def getSelfCardPosition(self, rank) -> (int, int):
        """

        :return:
        """
        pass

    @abstractmethod
    def get_three_landlord_cards_real(self):
        """

        :return: 三张底牌 这种样子[123]
        """

    @abstractmethod
    def get_self_turn(self):
        """

        :return: 返回是否是我的回合，意思是如果要我出牌了就返回true，否则返回false
        """

    @abstractmethod
    def get_self_turn_over(self):
        """

        :return: 返回我的回合是否结束， 就是我出牌是否完成
        """