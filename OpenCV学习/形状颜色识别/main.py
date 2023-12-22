# coding=utf-8
# python detect_color.py --image example_shapes.png

# 导入一些python包
from shapedetector import ShapeDetector
from colorlabeler import ColorLabeler
import argparse
import imutils
import cv2

# 读取图片
image = cv2.imread('count.png')
# 进行裁剪操作
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# 进行高斯模糊操作
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
# 进行图片灰度化
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
# 进行颜色空间的变换
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
# 进行阈值分割
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
cv2.imshow("Thresh", thresh)

# 在二值图片中寻找轮廓
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# 初始化形状检测器和颜色标签
sd = ShapeDetector()
cl = ColorLabeler()

# 遍历每一个轮廓
for c in cnts:
    # 计算每一个轮廓的中心点
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)

    # 进行颜色检测和形状检测
    shape = sd.detect(c)
    color = cl.label(lab, c)

    # 进行坐标变换
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    text = "{} {}".format(color, shape)
    # 绘制轮廓并显示结果
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
