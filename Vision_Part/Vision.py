from abc import ABC

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
        self.pointer_three_hand = []
        self.pointer_up_in = []
        self.pointer_down_in = []
        self.pointer_button = []
        self.pointer_pos0 = []  # 我的位置
        self.pointer_pos1 = []  # 我的上家
        self.pointer_pos2 = []  # 我的下家
        model.game_areas = {'self_player': self.pointer_pos0,
                            'next_player': self.pointer_pos1,
                            'last_player': self.pointer_pos2,
                            'public_area': self.pointer_three_hand}

    def whether_my_turn(self):
        if getSelfButtonPosition("pass"):
            return True
        else:
            return False

    def get_user_hand_card_in(self):
        user_hands_string = ""
        for i in range(15):
            for j in range(Game.players[0].deck.deck[i]):
                user_hands_string += EnvCard2RealCard[i]

        return user_hands_string

    def get_user_position_in(self):
        for i in range(3):
            if Game.players[i].character == 0:
                if (i == 0):
                    return "landlord"
                elif (i == 1):
                    return "landlord_up"
                else:
                    return "landlord_down"

    def get_three_landlord_cards_real(self):
        tmp_list = getHoleCards()
        s = ""
        for i in range(15):
            s += tmp_list[i] * EnvCard2RealCard[i]
        return s

    def get_down_in(self):
        return getLastPlayedCards(1)

    def get_up_in(self):
        return getLastPlayedCards(2)

    def image_in(self, image_in):
        updateScreen(image_in)


if __name__ == '__main__':
    Vision_my = Vision()
    image = cv.imread("C:\\Users\\21525\\Desktop\\3.png")
    Vision_my.image_in(image)
    print(Vision_my.get_user_hand_card_in())
