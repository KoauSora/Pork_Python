import threading
from abc import ABC, abstractmethod


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

    @abstractmethod
    def get_ready(self):
        """
        表示可以开始截屏的函数，主要提供给前端调用
        :return:
        """
        pass

    @abstractmethod
    def not_ready(self):
        """
        无需截屏，提供给前端使用
        :return:
        """
        pass
