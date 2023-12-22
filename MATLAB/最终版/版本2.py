import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt

file = pd.ExcelFile("C:\\Users\\33398\\Desktop\\cumcm2023problems\\A题\\附件.xlsx")
df = file.parse('Sheet1')

# 太阳时角
# 输入量是北京时间，输出太阳时角的弧度值
def W(Tm):
    # Tm使用本地时间即可
    W = np.pi * (Tm - 12) / 12

    return W


# 太阳赤纬角
# 输入量是一年中的哪一天，输出太阳赤纬角的弧度值
def Th(D):
    D -= 80
    if D < 0:
        D += 365

    sin_th = np.sin(2 * np.pi * D / 365) * np.sin(2 * np.pi * 23.45 / 360)  # 太阳赤纬角th的sin值
    hudu_th = m.asin(sin_th)  # 太阳赤纬角th的弧度值

    return hudu_th


# 太阳高度角
# 输入量是一年中的哪一天和一天中的哪个时刻，输出太阳高度角的弧度值
def As(D,tm):
    jiaodu_as = 90 * (np.pi / 180) - np.arccos(np.cos(Th(D))*np.cos(39.4*np.pi/180)*np.cos(W(tm)) + np.sin(Th(D))*np.sin(39.4*np.pi/180))
    hudu_as = jiaodu_as * 180 / np.pi

    return hudu_as
# 冬至到夏至 高度角逐渐增加

# 太阳辐射热量
# 输入量是一年中的哪一天和一天中的哪个时刻，输出太阳辐射热量的弧度值
def QDNI(D,tm):
    G0 = 1.366; # 太阳常数
    H = 3; # 海拔高度
    a = 0.4237 - 0.00821*((6-H)**2) # 大气压强
    b = 0.5055 + 0.00595*((6.5-H)**2) # 大气压强
    c = 0.2711 + 0.01858*((2.5-H)**2) # 大气压强
    DNI = G0*(a+b*np.exp(-c/np.sin(As(D,tm))))

    return DNI

Date = list(range(21, 366, 30))
Time = list(range(9, 15, 1))
DB9 = []
DB10 = []
DB11 = []
DB12 = []
DB13 = []
DB14 = []
for i in Date:
    for j in Time:
        print("Date: ", i, "Time: ", j, "AS:", As(i,j), "QDNI: ", QDNI(i, j))
        if j == 9 and QDNI(i,j) < 100:
            DB9.append(QDNI(i, j))
        elif j == 10 and QDNI(i,j) < 100:
            DB10.append(QDNI(i, j))
        elif j == 11 and QDNI(i,j) < 100:
            DB11.append(QDNI(i, j))
        elif j == 12 and QDNI(i,j) < 100:
            DB12.append(QDNI(i, j))
        elif j == 13 and QDNI(i,j) < 100:
            DB13.append(QDNI(i, j))
        elif j == 14 and QDNI(i,j) < 100:
            DB14.append(QDNI(i, j))

plt.figure()
plt.plot(range(0,len(DB9)), DB9, label='9')
# plt.plot(range(0,len(DB10)), DB10, label='10')
# plt.plot(range(0,len(DB11)), DB11, label='11')
# plt.plot(range(0,len(DB12)), DB12, label='12')
# plt.plot(range(0,len(DB13)), DB13, label='13')
# plt.plot(range(0,len(DB14)), DB14, label='14')
plt.legend()
plt.show()