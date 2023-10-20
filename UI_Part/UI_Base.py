import threading


class UI_Base:
    Lock_Image = threading.Lock()
    screenshot_image_list = []
    screenshot_image = None
    list = None

    def __init__(self):
        print("此类中的函数支持多线程运行")
        print("this is UI_Base init()!")

    def screen_shot(self):
        print("此函数用来获取当前屏幕的图像，先存放在一个变量中，并且维护了一个list用来存放未处理的图片")
        print("Please rewrite this function(UI_Base::get_mat() )!!!")

    def get_mat(self):
        print("此函数用来获取存储的图像如果图像被获取了，就从 变量 或者 list 中删除")
        print("Please rewrite this function(UI_Base::get_mat() )!!!")

    def get_ready(self):
        print("Please rewrite this function(UI_Base::get_ready() )!!!")
