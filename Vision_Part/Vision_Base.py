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
