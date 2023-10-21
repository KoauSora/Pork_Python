
import time


# modified by XuEddie

import cv2 as cv
import torch

import threading
import concurrent.futures

from UI_Part.Ui import UI
from UI_Part.UI_Widgets import MyApp


# rewrite by yuanshen


complet_result = []

event3 = threading.Event()
Run_or_Not = False


def function1():
    # 这里用来处理图像并且输出处理的结果,以下是测试程序

    event3.wait()
    time.sleep(10)
    print("开始执行线程1！")

# 这里是添加分析函数的地方my_task中执行需要分析的函数，提供了image的接口，这将返回一张图片，请使用此变量进行操作
    def my_task(image):
        if image is None:
            pass
            # print("image is None!")
        else:
            print("mytask")
            complet_result.append("123456")

    UI_object1 = UI()
    print(Run_or_Not)
    while Run_or_Not:
        # print("开始执行线程1的主题循环")
        while UI_object1.Ready:
            if UI_object1.need_more_thread():
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    print("这是多线程的结果")
                    futures = [executor.submit(my_task, UI_object1.get_mat()) for i in range(UI_object1.need_more_thread())]
            else:
                my_task(UI_object1.get_mat())
    print("执行完成")


def function2():
    # 这里用来并行的AI算法操作，以实现分析出牌，以下是测试程序
    output = torch.rand(3, 2)
    print(output)
    print("This is function2!")


def function3():
    # UI界面
    widgets = MyApp(400, 300)

    global Run_or_Not
    Run_or_Not = True
    print("开始执行")
    event3.set()

    widgets.run()
    Run_or_Not = False


thread1 = threading.Thread(target=function1)
thread2 = threading.Thread(target=function2)
thread3 = threading.Thread(target=function3)

thread3.start()
thread1.start()
thread2.start()

thread1.join()
thread2.join()
thread3.join()
