import cv2 as cv
import numpy
from PIL import ImageGrab  # 这个库用来实现截屏的UI
import threading

from UI_Part.UI_Base import UI_Base


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

    def get_ready(self):
        UI.Ready = True

    def not_ready(self):
        UI.Ready = False
