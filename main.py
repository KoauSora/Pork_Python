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
Run_or_Not = False


def change_result(text_in=""):
    with MyApp.Lock_text:
        MyApp.text_text = text_in
        print(MyApp.text_text)


def function1():
    # 这里用来处理图像并且输出处理的结果,以下是测试程序
    event3.wait()
    print("开始执行线程1！")

    class event_postion:
        """
        这是一个用来判断当前应该执行什么识别函数的类
        pos_func用来存放函数
        """

        def __init__(self):
            # self.pos_func = [initPlayers(), playCards(), getLastPlayedCards, getSelfCardPosition, getHoleCards,
            #                  getRestCards, getSelfButtonPosition]
            self.pos = 0

        def change_pos(self, pos_in):
            self.pos = pos_in

        def next_func(self):
            pass

        def last_func(self):
            pass

        def run_func(self):
            if self.pos == 0:
                pass
                # self.pos_func[self.pos]()
            elif self.pos == 1:
                pass
            elif self.pos == 2:
                pass

    event_need = event_postion()

    # 这里是添加分析函数的地方my_task中执行需要分析的函数，提供了image的接口，这将返回一张图片，请使用此变量进行操作
    def my_task(image):
        if image is None:
            pass
        else:
            updateScreen(image)
            initPlayers()
            print("身份是", Game.players[0].character, Game.players[1].character, Game.players[2].character, sep=" ")

    UI_object1 = UI()
    while Run_or_Not:
        # print("开始执行线程1的主题循环")
        while UI_object1.Ready:
            if UI_object1.need_more_thread():
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    # print("这是多线程的结果")
                    futures = [executor.submit(my_task, UI_object1.get_mat()) for i in
                               range(UI_object1.need_more_thread())]
            else:
                my_task(UI_object1.get_mat())
    print("线程1执行完成")


def function2():
    event2.wait()
    my_ai = AI_part()
    print("开始执行线程2")
    for i in range(10):
        time.sleep(2)
        output = torch.rand(3, 2)
        list_data = output.tolist()
        # 将列表转换为字符串
        str_data = str(list_data)
        change_result(str_data)

    # 在锁的保护下更新UI

    print("线程2执行完成")


def function3():
    widgets = MyApp(400, 300)
    print("开始执行线程3")
    global Run_or_Not
    Run_or_Not = True
    event3.set()
    event2.set()
    widgets.run()
    Run_or_Not = False
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
