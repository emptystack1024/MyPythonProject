# coding=utf-8
# 导入一些python包
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

# 创建一个颜色标签类
class ColorLabeler:
    def __init__(self):
        # 初始化一个颜色词典
        colors = OrderedDict({
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255)})

        # 为LAB图像分配空间
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

        # 循环 遍历颜色词典
        for (i, (name, rgb)) in enumerate(colors.items()):
            # 进行参数更新
            self.lab[i] = rgb
            self.colorNames.append(name)

        # 进行颜色空间的变换
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        # 根据轮廓构造一个mask，然后计算mask区域的平均值
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # 初始化最小距离
        minDist = (np.inf, None)

        # 遍历已知的LAB颜色值
        for (i, row) in enumerate(self.lab):
            # 计算当前l*a*b*颜色值与图像平均值之间的距离
            d = dist.euclidean(row[0], mean)

            # 如果当前的距离小于最小的距离，则进行变量更新
            if d < minDist[0]:
                minDist = (d, i)

        # 返回最小距离对应的颜色值
        return self.colorNames[minDist[1]]
