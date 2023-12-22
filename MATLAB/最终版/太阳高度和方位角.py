import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt

file = pd.ExcelFile("C:\\Users\\33398\\Desktop\\cumcm2023problems\\A题\\附件.xlsx")
df = file.parse('Sheet1')

# 太阳高度角
# 输入量是一年中的哪一天和一天中的哪个时刻，输出太阳高度角的弧度值
def As(D,tm):

    # 太阳的赤纬角 th
    # 输入量是一年中的哪一天，输出太阳赤纬角的弧度值
    D -= 80
    if D < 0:
        D += 365
    sin_th = np.sin(2 * np.pi * D / 365) * np.sin(2 * np.pi * 23.45 / 360)  # 太阳赤纬角th的sin值
    th = m.asin(sin_th)  # 太阳赤纬角th的弧度值

    omg = 39.4/180*np.pi # 本地纬度

    w = np.pi * (tm- 12) / 12 # 太阳时

    a_s = np.cos(th)*np.cos(omg)*np.cos(w)+np.sin(th)*np.sin(omg) # 太阳高度角的sin值
    hudu_as = m.asin(a_s) # 太阳高度角的弧度值
    jiaodu_as = hudu_as*180/np.pi # 太阳高度角的角度值

    return jiaodu_as

Date = list(range(1, 366, 30))
Time = list(range(9, 15, 1))
Plat = []

for i in Date:
    for j in Time:
        print("Date: ", i, "Time: ", j, "As: ", As(i, j))
        Plat.append(As(i, j))
