import cv2
import numpy as np

if __name__ == '__main__':

    # 读取图像
    image = cv2.imread("template/pic2.png")
    # print(image)
    print(1)
    # 颜色选择
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([100, 100, 255])
    mask = cv2.inRange(image, lower_red, upper_red)
    result = cv2.bitwise_and(image, image, mask=mask)

    # cv2.imshow('Result', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray)

    gray2 = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    equalized_image2 = cv2.equalizeHist(gray)

    # kernel = np.ones((3, 3), np.uint8)
    # # 膨胀操作
    # dilated = cv2.dilate(equalized_image, kernel, iterations=1)

    cv2.imshow('Result1', equalized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 二值化
    _, binary_image = cv2.threshold(equalized_image, 100, 255, cv2.THRESH_BINARY)
    _, binary_image2 = cv2.threshold(equalized_image2, 50, 255, cv2.THRESH_BINARY)

    cv2.imshow('Result2', binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # 形态学转换
    # cv2.imshow('Result', binary_image2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # kernel = np.ones((5, 5), np.uint8)
    # dilated = cv2.dilate(binary_image, kernel, iterations=1)
    # eroded = cv2.erode(dilated, kernel, iterations=1)

    # cv2.imshow('Result', eroded)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 轮廓检测
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(binary_image2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 提取数字区域
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # 过滤掉过小的区域
        # if w > 5 and h > 20:
            # 在原图上绘制矩形
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        digit_region = binary_image[y:y + h, x:x + w]

        # 在这里可以添加数字识别的代码，例如使用模型进行识别

    # 显示结果图像
    #
    cv2.imshow('Result3', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
