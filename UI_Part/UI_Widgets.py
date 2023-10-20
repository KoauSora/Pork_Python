import tkinter
import time

from UI_Part.Ui import UI
from UI_Part.UI_Widgets_Base import MyApp_Base


class MyApp(MyApp_Base):

    def __init__(self, Length_in, Height_in):
        super().__init__(Length_in, Height_in)

        self.interval = 2

        self.root = tkinter.Tk()
        self.root.title("Pork_AI")
        self.root.geometry(f"{Length_in}x{Height_in}")

        # 创建一个开始按钮
        self.start_button = tkinter.Button(self.root, text="开始", width=5,height=2,command=self.start_button_clicked)
        self.start_button.pack()

        # 创建一个标签用于显示操作结果
        self.result_label = tkinter.Label(self.root, text="")
        self.result_label.pack()

    def change_interval(self, interval_in):
        self.interval = interval_in

    def start_button_clicked(self):
        # 在这里执行您希望在点击按钮后执行的操作
        self.result_label.config(text="操作已执行")
        UI_object = UI()
        for i in range(5):
            UI_object.screen_shot()
            time.sleep(self.interval)
            print("This is function3!")

    def run(self):
        # 开始主事件循环
        self.root.mainloop()
