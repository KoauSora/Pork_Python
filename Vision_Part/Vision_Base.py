from abc import ABC, abstractmethod
# from model import *

EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q',
                    13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'}

RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                    '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                    'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30}


class VisionVirtualBase(ABC):
    # @abstractmethod
    # def getGameStatus(self):
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def getPlayerCharacter(self, position):
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def getPlayerDeck(self, position) -> Deck:
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def getRestCard(self) -> list[int]:
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def getSelfPlayerStatus(self):
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def getSelfCardsPositions(self):
    #     """
    #
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # def getSelfCardPosition(self, rank) -> (int, int):
    #     """
    #
    #     :return:
    #     """
    #     pass

    @abstractmethod
    def get_user_hand_card_in(self):
        """

        :return: 字符串类型 "A23456789TJQKXD"
        """
        pass

    @abstractmethod
    def get_user_position_in(self):
        """

        :return: 字符串 'landlord_up', 'landlord', 'landlord_down'
        """
        pass

    @abstractmethod
    def get_three_landlord_cards_real(self):
        """

        :return: 同上
        """
        pass

    @abstractmethod
    def get_down_in(self):
        """

        :return: 下家出的牌
        """
        pass

    @abstractmethod
    def get_up_in(self):
        """

        :return: 上家出牌
        """
        pass

    @abstractmethod
    def image_in(self, image_in):
        """

        :param image_in: 图片
        :return:
        """

    @abstractmethod
    def position_in(self, point_in):
        """

        :param point_in: [1,2,3,4]
        :return:
        """

    @abstractmethod
    def whether_my_turn(self):
        """

        :return: True 是我的轮次 False 不是我的轮次
        """
