import time
import cv2 as cv
import torch
import threading
import concurrent.futures
from UI_Part.Ui import UI
from UI_Part.UI_Widgets import MyApp
from Vision_Part.process import *
from AI_Part.AI_part import *

# 这个是线程的阻塞机制，用来调整线程的先后关系
event3 = threading.Event()
event2 = threading.Event()


# 此变量表示是否有必要继续存在function1，来处理图片，当窗口关闭的时候变为false


class event_postion:
    """
    :Run_or_Not  表示当前UI部分是否开始运行
    :pos 表示当前的执行函数 wait for writing
    :user_position_in: 'landlord_up', 'landlord', 'landlord_down'
    :three_landlord_cards_real: 同下
    :user_hand_card_in: example :假设有 2 个 2 ，两个A ，三个 3 ，则输入'22AA333'
    :player_order_in: 出牌顺序：0-玩家先出牌, 1-玩家下家先出牌, 2-玩家上家先出牌
    :down_in: 玩家下家的牌，如三个A 则输入“AAA”
    :up_in: 玩家上家的牌，同上
    """
    UI_object1 = None
    Run_or_Not = False

    pos = 0
    user_hand_card_in = ""
    user_position_in = ""
    three_landlord_cards_real = ""
    player_order_in = 0
    down_in = ""
    up_in = ""
    over = False

    def UI_start(self):
        event_postion.UI_object1 = UI()


    def __init__(self):
        # self.pos_func = [initPlayers(), playCards(), getLastPlayedCards, getSelfCardPosition, getHoleCards,
        #                  getRestCards, getSelfButtonPosition]
        self.image = None

    def change_pos(self, pos_in):
        self.pos = pos_in

    def next_func(self):
        pass

    def last_func(self):
        pass

    def run_func(self, image_in):
        if event_postion.over:
            return
        self.image = image_in
        if self.pos == 0:
            updateScreen(self.image)
            initPlayers()
            print("身份是", Game.players[0].character, Game.players[1].character, Game.players[2].character, sep=" ")

            # self.pos_func[self.pos]()
        elif self.pos == 1:
            pass
        elif self.pos == 2:
            pass

    def change_result(self, text_in=""):
        with MyApp.Lock_text:
            MyApp.text_text = text_in
            print(MyApp.text_text)


def function1():
    # 这里用来处理图像并且输出处理的结果,以下是测试程序
    event3.wait()
    print("开始执行线程1！")
    event_need = event_postion()
    event_need.UI_start()

    # 这里是添加分析函数的地方my_task中执行需要分析的函数，提供了image的接口，这将返回一张图片，请使用此变量进行操作
    def my_task(image):
        if image is None:
            pass
        else:
            # 表示当前应该运行的函数，通过此类中的pos进行改变
            event_need.run_func(image)
            # updateScreen(image)
            # initPlayers()
            # print("身份是", Game.players[0].character, Game.players[1].character, Game.players[2].character, sep=" ")
    print("function1:")
    print(event_postion.Run_or_Not)

    while event_postion.Run_or_Not:
        # print("开始执行线程1的主题循环")
        while event_postion.UI_object1.Ready:
            if event_postion.UI_object1.need_more_thread():
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    # print("这是多线程的结果")
                    futures = [executor.submit(my_task, event_postion.UI_object1.get_mat()) for i in
                               range(event_postion.UI_object1.need_more_thread())]
            else:
                my_task(event_need.UI_object1.get_mat())
    print("线程1执行完成")


def function2():
    event2.wait()
    event_need = event_postion()
    my_ai = AI_part()
    print("开始执行线程2")

    print("function2:")
    print(event_need.Run_or_Not)

    while event_postion.Run_or_Not:
        while event_postion.UI_object1.Ready:
            if event_postion.pos == 0:

                pass
            elif event_postion.pos == 1:
                pass
            time.sleep(2)
            output = torch.rand(3, 2)
            list_data = output.tolist()
            # 将列表转换为字符串
            str_data = str(list_data)
            event_need.change_result(str_data)

    # 在锁的保护下更新UI

    print("线程2执行完成")


def function3():
    widgets = MyApp(400, 300)
    print("开始执行线程3")

    event_postion.Run_or_Not = True
    event3.set()
    event2.set()
    widgets.run()
    event_postion.Run_or_Not = False
    print("线程3执行完成")


if __name__ == '__main__':
    thread1 = threading.Thread(target=function1)
    thread2 = threading.Thread(target=function2)
    thread3 = threading.Thread(target=function3)

    thread3.start()
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    thread3.join()
