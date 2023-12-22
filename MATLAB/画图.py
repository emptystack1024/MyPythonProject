import numpy as np
import math as m
import pandas as pd
import matplotlib.pyplot as plt

file = pd.ExcelFile("C:\\Users\\33398\\Desktop\\cumcm2023problems\\A题\\附件.xlsx")
df = file.parse('Sheet1')

h = 1.2923 # D = 90
th = 3.1416

R_x = -np.cos(h) * np.sin(th)
R_y = -np.cos(h) * np.cos(th)
R_z = -np.sin(h)

print("R_x: ", R_x)
print("R_y: ", R_y)
print("R_z: ", R_z)

# 求效率总值
sum = 0
DB = []

for i in range(0, 1745):
    # 镜子的xy坐标
    x = df.iloc[i, 0]
    y = df.iloc[i, 1]
    # 出射光的向量m
    test = np.array([x, y, 80])

    # 入射光的方向向量
    S = np.array([2.0196, -0.2749, -0.9614])
    # S = np.array([R_x, R_y, R_z])

    # 归一化入射光线和出射光线的方向向量
    test_unit = test / np.linalg.norm(test)
    S_unit = S / np.linalg.norm(S)

    temp = np.arccos(np.dot(S_unit,test_unit))
    temp /= 2
    temp = np.cos(temp)
    print(str(i) + " " + str(temp))
    DB.append(temp)
    sum += temp

sum /= len(df)
print("效率总值：", sum)

x = np.arange(0, 1745, 1)
plt.plot(x, DB)

plt.title("cos效率")
plt.xlabel("序号")
plt.ylabel("效率")

plt.grid(True)
plt.show()