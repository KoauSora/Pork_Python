import torch
import torchvision
import cv2
import numpy as np
# 加载图像

def preProccessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    imgDial = cv2.dilate(imgCanny, np.ones((5, 5)), iterations=2)  # 膨胀操作
    imgThres = cv2.erode(imgDial, np.ones((5, 5)), iterations=1)  # 腐蚀操作
    return imgThres


def getContours(img):
    x, y, w, h, xx, yy, ss = 0, 0, 10, 10, 20, 20, 10  # 因为图像大小不能为0
    imgGet = np.array([[], []])  # 不能为空
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 检索外部轮廓
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 800:  # 面积大于800像素为封闭图形
            cv2.drawContours(imgCopy, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)  # 计算周长
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # 计算有多少个拐角
            x, y, w, h = cv2.boundingRect(approx)  # 得到外接矩形的大小
            # a = (w + h) // 2
            # dd = abs((w - h) // 2)  # 边框的差值
            # imgGet = imgProcess[y:y + h, x:x + w]
            # if w <= h:  # 得到一个正方形框，边界往外扩充20像素,黑色边框
            #     imgGet = cv2.copyMakeBorder(imgGet, 20, 20, 20 + dd, 20 + dd, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            #     xx = x - dd - 10
            #     yy = y - 10
            #     ss = h + 20
            #     cv2.rectangle(imgCopy, (x - dd - 10, y - 10), (x + a + 10, y + h + 10), (0, 255, 0),
            #                   2)  # 看看框选的效果，在imgCopy中
            #     print(a + dd, h)
            # else:  # 边界往外扩充20像素值
            #     imgGet = cv2.copyMakeBorder(imgGet, 20 + dd, 20 + dd, 20, 20, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            #     xx = x - 10
            #     yy = y - dd - 10
            #     ss = w + 20
            #     cv2.rectangle(imgCopy, (x - 10, y - dd - 10), (x + w + 10, y + a + 10), (0, 255, 0), 2)
            #     print(a + dd, w)
            Temptuple = (imgGet, x, y, w, h)  # 将图像及其坐标放在一个元组里面，然后再放进一个列表里面就可以访问了
            Borderlist.append(Temptuple)

    return Borderlist

Borderlist = []  # 不同的轮廓图像及坐标
Resultlist = []  # 识别结果
img = cv2.imread("C:\\Users\\HP\\PycharmProjects\\Pork_Python-main\\Study_Part\\Sudy_Part_Vision\\template\\9.png", 1)
imgCopy = img.copy()
imgProcess = preProccessing(img)
Borderlist = getContours(imgProcess)
# 遍历 Borderlist 列表，并访问每个元组中的图像和坐标
for item in Borderlist:
    img = item[0]  # 获取图像
    x = item[1]  # 获取 xx 坐标
    print(x)
    y = item[2]  # 获取 yy 坐标
    print(y)
    w = item[3]  # 获取字符串 ss
    h = item[4]
    print(w)
    print(h)
    print("over")

x1 = 0  # 左上角 x 坐标
y1 = 0  # 左上角 y 坐标
x2 = 200 # 右下角 x 坐标
y2 = 200 # 右下角 y 坐标
cropped_image = img[y1:y2, x1:x2]

    # 显示截取的图像
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()