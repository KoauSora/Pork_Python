from abc import ABC

from Pork_Python.Vision_Part import model
from Pork_Python.Vision_Part.Vision_Base import VisionVirtualBase
import cv2 as cv
import numpy as np
from Pork_Python.Vision_Part.process import *
from Pork_Python.Vision_Part.model import *

EnvCard2RealCard = {0: '3', 1: '4', 2: '5', 3: '6', 4: '7',
                    5: '8', 6: '9', 7: 'T', 8: 'J', 9: 'Q',
                    10: 'K', 11: 'A', 12: '2', 13: 'X', 14: 'D'}


# 预处理
def prepare_for_pic(image_in):
    """

    :param image_in: 传入的图片
    :return: [[x,y,h,w],[...]...]
    """


def get_pre_pic(pointer, num_in):
    """

    :param num_in: 图片的位置
    :param pointer: [[x,y,h,w],[...]...]
    :return: image(图片)
    """


class Vision:
    def __init__(self):
        self.pointer_user_hands = [0, 0, 1, 1]  # y1,y2,x1,x2
        self.pointer_three_hand = [0, 0, 1, 1]
        self.pointer_up_in = [0, 0, 1, 1]
        self.pointer_down_in = [0, 0, 1, 1]
        self.pointer_button = [0, 0, 1, 1]
        self.pointer_pos0 = [0, 0, 1, 1]  # 我的位置
        self.pointer_pos1 = [0, 0, 1, 1]  # 我的上家
        self.pointer_pos2 = [0, 0, 1, 1]  # 我的下家
        model.Game.game_areas = {'self_player': self.pointer_pos0,
                                 'next_player': self.pointer_pos1,
                                 'last_player': self.pointer_pos2,
                                 'public_area': self.pointer_three_hand}

    @staticmethod
    def whether_my_turn():
        if getSelfButtonPosition("pass"):
            return True
        else:
            return False

    @staticmethod
    def get_user_hand_card_in():
        user_hands_string = ""
        for i in range(15):
            for j in range(Game.players[0].deck.deck[i]):
                user_hands_string += EnvCard2RealCard[i]
        # print(user_hands_string)
        return user_hands_string

    @staticmethod
    def get_user_position_in():
        for i in range(3):
            if Game.players[i].character == 0:
                if i == 0:
                    return "landlord"
                elif i == 1:
                    return "landlord_up"
                else:
                    return "landlord_down"

    @staticmethod
    def get_three_landlord_cards_real():
        tmp_list = getHoleCards()
        s = ""
        for i in range(15):
            s += tmp_list[i] * EnvCard2RealCard[i]
        return s

    @staticmethod
    def get_down_in():
        tmp_list = getLastPlayedCards(1)
        playCards(1, tmp_list)
        s = ""
        for i in range(15):
            s += tmp_list[i] * EnvCard2RealCard[i]
        return s

    @staticmethod
    def get_up_in():
        tmp_list = getLastPlayedCards(2)
        playCards(2, tmp_list)
        s = ""
        for i in range(15):
            s += tmp_list[i] * EnvCard2RealCard[i]
        return s

    @staticmethod
    def image_in(image_in):
        updateScreen(image_in)

