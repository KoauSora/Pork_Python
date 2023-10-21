import threading
from abc import ABC, abstractmethod


class UI_Base(ABC):
    @abstractmethod
    def screen_shot(self):
        pass

    @abstractmethod
    def get_mat(self):
        pass

    @abstractmethod
    def need_more_thread(self):
        pass

    @abstractmethod
    def get_ready(self):
        pass

    @abstractmethod
    def not_ready(self):
        pass
