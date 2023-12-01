import concurrent.futures
from abc import ABC, abstractmethod
import cv2 as cv
import numpy
from PIL import ImageGrab  # 这个库用来实现截屏的UI
import tkinter
import time
import threading

from AI_Part.AI_part import *
from Vision_Part.Vision import Vision
from Vision_Part.process import initPlayers


class UI_Base(ABC):
    @abstractmethod
    def screen_shot(self):
        """
        这个函数用来截取屏幕图像
        :return: None
        """
        pass

    @abstractmethod
    def get_mat(self):
        """
        支持多线程的获取图片函数
        :return: cv.image
        """
        pass

    @abstractmethod
    def need_more_thread(self):
        """
        当list中存在内容时，进行多线程并行运算
        :return:
        """
        pass


class UI(UI_Base):
    Ready = False
    Lock_Image = threading.Lock()
    screenshot_image_list = []
    screenshot_image = None
    list = None

    def __init__(self):
        super().__init__()

    def screen_shot(self):
        screenshot = ImageGrab.grab()
        numpy_screenshot = numpy.array(screenshot)
        with UI.Lock_Image:
            if UI.screenshot_image is None:
                UI.screenshot_image = cv.cvtColor(numpy_screenshot, cv.COLOR_RGB2BGR)
            else:
                UI.screenshot_image_list.append(cv.cvtColor(numpy_screenshot, cv.COLOR_RGB2BGR))

    def get_mat(self):
        with UI.Lock_Image:
            if UI.screenshot_image is None:
                return None
            else:
                if len(UI.screenshot_image_list) == 0:
                    temp = UI.screenshot_image
                    UI.screenshot_image = None
                    return temp
                else:
                    temp = UI.screenshot_image
                    UI.screenshot_image = UI.screenshot_image_list[0]
                    UI.screenshot_image_list.pop(0)
                    return temp

    def need_more_thread(self):
        with UI.Lock_Image:
            if len(UI.screenshot_image_list) != 0:
                return len(UI.screenshot_image_list)
            else:
                return False

    @staticmethod
    def get_ready():
        UI.Ready = True

    @staticmethod
    def not_ready():
        UI.Ready = False


class MyApp_Base(ABC):
    @abstractmethod
    def start_button_clicked(self):
        pass

    @abstractmethod
    def stop_button_clicked(self):
        pass

    @abstractmethod
    def run_program(self):
        pass

    @abstractmethod
    def run(self):
        pass


class MyApp(MyApp_Base):
    UI_object = UI()
    text_text = "..."
    Lock_text = threading.Lock()

    def __init__(self, Length_in, Height_in):
        self.interval = 2

        self.Run_or_not = False
        self.Run_program_start = False

        self.root = tkinter.Tk()
        self.root.title("Pork_AI")
        self.root.geometry(f"{Length_in}x{Height_in}")

        # 创建一个开始按钮
        self.start_button = tkinter.Button(self.root, text="开始", width=5, height=2, command=self.start_button_clicked)
        self.start_button.pack()

        self.stop_button = tkinter.Button(self.root, text="结束", width=5, height=2, command=self.stop_button_clicked)
        self.stop_button.config(state="disabled")
        self.stop_button.pack()

        # 创建一个标签用于显示操作结果
        self.result_label = tkinter.Label(self.root, text="")
        self.result_label.pack()

        # 创建一个标签用来显示出牌和胜率
        self.cards_result = tkinter.Label(self.root, text=MyApp.text_text)
        self.cards_result.pack()

        # 这是一个线程
        self.program_thread = None

    def change_interval(self, interval_in):
        self.interval = interval_in

    def update_label(self):
        with MyApp.Lock_text:
            self.cards_result.config(text=MyApp.text_text)
            # print("update:")
            # print(MyApp.text_text)
        self.root.after(500, self.update_label)

    def start_button_clicked(self):
        # 在这里执行您希望在点击按钮后执行的操作
        self.result_label.config(text="操作已执行")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        UI.get_ready()
        # print(MyApp.UI_object.Ready)
        self.program_thread = threading.Thread(target=self.run_program)
        self.program_thread.start()

    def stop_button_clicked(self):
        self.result_label.config(text="操作已经停止")
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        UI.not_ready()

    def run_program(self):
        self.Run_program_start = True
        while UI.Ready and self.Run_or_not:
            MyApp.UI_object.screen_shot()
            print("This is screenshot function!")
            time.sleep(self.interval)
            # print(UI.Ready)

    def on_closing(self):
        self.stop_button_clicked()
        self.Run_or_not = False
        if self.Run_program_start is True:
            self.program_thread.join()
        self.root.destroy()

    def run(self):
        # 开始主事件循环
        self.Run_or_not = True
        self.update_label()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    @staticmethod
    def change_result():
        UI.get_ready()


# 这个是线程的阻塞机制，用来调整线程的先后关系
event3 = threading.Event()
event2 = threading.Event()


# 此变量表示是否有必要继续存在function1，来处理图片，当窗口关闭的时候变为false
class event_postion:
    """
    :Run_or_Not  表示当前UI部分是否开始运行
    :pos 表示当前的执行函数 pos = 0 代表 识别三张底牌，地主位置，玩家初始手牌，
    :user_position_in: 'landlord_up', 'landlord', 'landlord_down'
    :three_landlord_cards_real: 同下
    :user_hand_card_in: example :假设有 2 个 2 ，两个A ，三个 3 ，则输入'22AA333'
    :player_order_in: 出牌顺序：0-玩家先出牌, 1-玩家下家先出牌, 2-玩家上家先出牌
    :down_in: 玩家下家的牌，如三个A 则输入“AAA”
    :up_in: 玩家上家的牌，同上
    """
    real2pos = {'landlord': 0, 'landlord_up': 1, 'landlord_down': 2}

    Run_or_Not = False
    Vision_object = Vision()
    UI_object1 = UI()
    whether_lock = threading.Lock()

    pos = 0
    user_hand_card_in = ""
    user_position_in = ""
    three_landlord_cards_real = ""
    down_in = ""
    up_in = ""
    over = False
    flag = -1
    whether_my_turn = False

    def __init__(self):
        pass

    def change_pos(self, pos_in):
        self.pos = pos_in

    def next_func(self):
        pass

    def last_func(self):
        pass

    def run_func(self, image_in):
        # print(1)
        if event_postion.over:
            return
        Vision.image_in(image_in)

        if self.pos == 0:
            # print(1)
            initPlayers()
            event_postion.three_landlord_cards_real = event_postion.Vision_object.get_three_landlord_cards_real()
            # print(event_postion.three_landlord_cards_real + '\n')
            event_postion.user_position_in = event_postion.Vision_object.get_user_position_in()
            print(event_postion.user_position_in)
            event_postion.user_hand_card_in = event_postion.Vision_object.get_user_hand_card_in()
            print(event_postion.user_hand_card_in)
            event_postion.player_order_in = event_postion.real2pos[event_postion.user_position_in]
        elif self.pos == 1:
            event_postion.up_in = event_postion.Vision_object.get_up_in()
            event_postion.down_in = event_postion.Vision_object.get_down_in()
        elif self.pos == 2:
            event_postion.over = True

    @staticmethod
    def change_result(text_in=""):
        with MyApp.Lock_text:
            MyApp.text_text = text_in


def function1():
    # 这里用来处理图像并且输出处理的结果,以下是测试程序
    event3.wait()
    print("开始执行线程1！")
    event_need = event_postion()

    # 这里是添加分析函数的地方my_task中执行需要分析的函数，提供了image的接口，这将返回一张图片，请使用此变量进行操作
    def my_task(image):
        if image is None:
            pass
        else:
            # 表示当前应该运行的函数，通过此类中的pos进行改变
            # print(image)
            event_need.run_func(image)
            # with event_postion.whether_lock:
            #     event_postion.whether_my_turn = event_postion.Vision_object.whether_my_turn()

    print("function1:")

    while event_postion.Run_or_Not:
        # print("开始执行线程1的主题循环")
        while UI.Ready:
            if event_postion.UI_object1.need_more_thread():
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    # print("这是多线程的结果")
                    futures = [executor.submit(my_task, event_postion.UI_object1.get_mat()) for i in
                               range(event_postion.UI_object1.need_more_thread())]
            else:
                my_task(event_postion.UI_object1.get_mat())
    print("线程1执行完成")


def function2():
    event2.wait()
    my_ai = AI_part()
    print("开始执行线程2")
    flag_2 = False
    print("function2:")
    # print(event_need.Run_or_Not)
    while event_postion.Run_or_Not:
        while UI.Ready:
            print(event_postion.pos)
            # print(event_postion.user_hand_caintrd_in)
            if event_postion.pos == 0 and event_postion.user_hand_card_in != "":
                # print(2)
                my_ai.init_cards(event_postion.user_hand_card_in, event_postion.user_position_in,
                                 event_postion.three_landlord_cards_real)
                my_ai.init_players()
                my_ai.init_Env()
                my_ai.play_order = event_postion.real2pos[event_postion.user_position_in]
                flag_2 = True
                event_postion.pos = 1
            if flag_2:
                # print(3)
                with event_postion.whether_lock:
                    if event_postion.whether_my_turn:
                        event_postion.flag += 1
                        # print(1.1)
                    else:
                        event_postion.flag = -1
                if event_postion.flag == 0:
                    if event_postion.pos == 1:
                        # print(2)
                        my_ai.start_predict(event_postion.down_in, event_postion.up_in)
                        event_postion.change_result(my_ai.win_rate + ": " + my_ai.cards_out)
            time.sleep(2)
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
    # my = MyApp(400,300)
    # my.change_result()
    # UI_object2 = UI()
    # print(UI_object2.Ready)
