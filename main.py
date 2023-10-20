# modified by XuEddie
import cv2 as cv
import torch

import threading

from UI_Part.Ui import UI
from UI_Part.UI_Widgets import MyApp


# rewrite by yuanshen
def function1():
    # 这里用来处理图像并且输出处理的结果,以下是测试程序
    UI_object1 = UI()
    num = 0
    while num < 5:
        temp = UI_object1.get_mat()
        if temp is None:
            continue
        cv.imshow("pic", temp)
        cv.waitKey(0)
        print("This is function1!")
        num = num + 1


def function2():
    # 这里用来并行的AI算法操作，以实现分析出牌，以下是测试程序
    output = torch.rand(3, 2)
    print(output)
    print("This is function2!")


def function3():
    # UI界面
    widgets = MyApp(400, 300)
    widgets.run()


thread1 = threading.Thread(target=function1)
thread2 = threading.Thread(target=function2)
thread3 = threading.Thread(target=function3)

thread3.start()
thread1.start()
thread2.start()

thread1.join()
thread2.join()
thread3.join()
