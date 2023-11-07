import tkinter
import time
import threading

from UI_Part.Ui import UI
from UI_Part.UI_Widgets_Base import MyApp_Base


class MyApp(MyApp_Base):
    UI_object = UI()

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

        # 这是一个线程
        self.program_thread = None

    def change_interval(self, interval_in):
        self.interval = interval_in

    def start_button_clicked(self):
        # 在这里执行您希望在点击按钮后执行的操作
        self.result_label.config(text="操作已执行")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        MyApp.UI_object.get_ready()
        self.program_thread = threading.Thread(target=self.run_program)
        self.program_thread.start()

    def stop_button_clicked(self):
        self.result_label.config(text="操作已经停止")
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        MyApp.UI_object.not_ready()

    def run_program(self):
        self.Run_program_start = True
        while MyApp.UI_object.Ready and self.Run_or_not:
            MyApp.UI_object.screen_shot()
            print("This is screenshot function!")
            time.sleep(self.interval)

    def on_closing(self):
        self.stop_button_clicked()
        self.Run_or_not = False
        if self.Run_program_start is True:
            self.program_thread.join()
        self.root.destroy()

    def run(self):
        # 开始主事件循环
        self.Run_or_not = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
