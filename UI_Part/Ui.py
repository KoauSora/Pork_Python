import cv2 as cv
import numpy
from PIL import ImageGrab  # 这个库用来实现截屏的UI

from UI_Part.UI_Base import UI_Base


class UI(UI_Base):

    def __init__(self):
        super().__init__()

    def screen_shot(self):
        screenshot = ImageGrab.grab()
        numpy_screenshot = numpy.array(screenshot)
        with UI_Base.Lock_Image:
            if UI_Base.screenshot_image is None:
                UI_Base.screenshot_image = cv.cvtColor(numpy_screenshot, cv.COLOR_RGB2BGR)
            else:
                UI_Base.screenshot_image_list.append(cv.cvtColor(numpy_screenshot, cv.COLOR_RGB2BGR))

    def get_mat(self):
        with UI_Base.Lock_Image:
            if UI_Base.screenshot_image is None:
                return None
            else:
                if len(UI_Base.screenshot_image_list) == 0:
                    temp = UI_Base.screenshot_image
                    UI_Base.screenshot_image = None
                    return temp
                else:
                    temp = UI_Base.screenshot_image
                    UI_Base.screenshot_image = UI_Base.screenshot_image_list[0]
                    UI_Base.screenshot_image_list.pop(0)
                    return temp

    def get_ready(self):
        super().get_ready()
