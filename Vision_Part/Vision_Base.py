from enum import Enum


# 以下为枚举量SIZE，意为花色
class SIZE(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3
    NULL_SIZE = 4


# 以下为枚举量，POSITION,意为成员
class PLAYER(Enum):
    PLAYER1 = 0  # 地主
    PLAYER2 = 1  # 地主下家
    PLAYER3 = 2  # 地主上家


class PORK:
    def __init__(self, pos_in=None, value_in=None, size_in=None):
        self.my_pos = pos_in
        self.value_array = value_in
        self.size_array = size_in
        self.next = None


class recognize_part_VirtualBase:
    def __init__(self):
        self.pork_1 = None
        self.pork_2 = None
        self.pork_3 = None
        self.ready = False

    def Get_PORK1(self):
        return self.pork_1

    def Get_PORK2(self):
        return self.pork_2

    def Get_PORK3(self):
        return self.pork_3

    def Get_ready(self):
        print("Please rewrite this function(recognize_part_VirtualBase.Get_ready())!!!")
        raise NotImplementedError
        pass

    def change_ready_setting(self):
        self.ready = not self.ready
        pass
