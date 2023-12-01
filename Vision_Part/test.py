from recognize import *
import cv2

path = r"C:\Users\Kimin\Downloads\test.jpg"
img = cv2.imread(path)
print(getCardsInArea(img, [0, 0, 1 / 2, 1], show=True))
# getButtonPosition(img, 'others_pass')
