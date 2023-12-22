import cv2
import os
import numpy as np
from PIL import Image, ImageTk

def aHash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n

def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def calculate_similarity(image1, image2):
    image1=image1.split("/")[-2]+"/"+image1.split("/")[-1]
    image2=image2.split("/")[-2]+"/"+image2.split("/")[-1]
    print("image1:", image1)
    print("image2:", image2)
    # 方法1  均值哈希算法相似度 计算两张图像的相似度
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    hash1 = aHash(img1)
    hash2 = aHash(img2)
    similarity_1= cmpHash(hash1, hash2)

    # 方法2   差值哈希算法相似度 计算两张图像的相似度
    hash1 = dHash(img1)
    hash2 = dHash(img2)
    similarity_2= cmpHash(hash1, hash2)

    # 方法3 计算两张图像的相似度
    print("image1, image2:",image1, image2)
    image1 = np.array(Image.open(image1))
    image2 = np.array(Image.open(image2))
    arr1_flat = image1.reshape(-1)
    arr2_flat = image2.reshape(-1)
    num_equal = np.sum(arr1_flat == arr2_flat)
    similarity_3 = num_equal / len(arr1_flat)
    print('均值哈希算法相似度：', similarity_1,'差值哈希算法相似度：', similarity_2,"np.sum:",similarity_3)
    return similarity_1/100,similarity_2/100,similarity_3

img_name = r'C:\code\pythonProject\jupy_test\OpenCV学习\实验3\Library\2.png'
img = cv2.imread(img_name)

folder = os.path.dirname(img_name)
filenames = os.listdir(folder)
filenames = [f'{folder}/{f}' for f in filenames if f.endswith('.png')]
for i in range(len(filenames)):
    print("filenames:",filenames[i])
filenames.remove(img_name)

# 三种不同的方法的相似度数组
similarities1 = []
similarities2 = []
similarities3 = []
for filename in filenames:
    print("filename : ",filename)
    similarity1, similarity2, similarity3 = calculate_similarity(img_name, filename)
    similarities1.append(similarity1)
    similarities2.append(similarity2)
    similarities3.append(similarity3)

# 根据相似度从高到低排序，并取出前三个最相似的图像
similarities1.sort(key=lambda x: x[1], reverse=False)
similarities2.sort(key=lambda x: x[1], reverse=False)
similarities3.sort(key=lambda x: x[1], reverse=True )# 这个没问图

imgs1 = [similarities1[0:3]]
imgs2 = [similarities2[0:3]]
imgs3 = [similarities3[0:3]]

# 将imgs1中的图片拼接
img1 = cv2.imread(img_name)
for i in range(3):
    img1 = np.hstack((img1, cv2.imread(imgs1[0][i])))
cv2.imshow('img1', img1)

# 将imgs2中的图片拼接
img2 = cv2.imread(img_name)
for i in range(3):
    img2 = np.hstack((img2, cv2.imread(imgs2[0][i])))
cv2.imshow('img2', img2)

# 将imgs3中的图片拼接
img3 = cv2.imread(img_name)
for i in range(3):
    img3 = np.hstack((img3, cv2.imread(imgs3[0][i])))
cv2.imshow('img3', img3)

cv2.waitKey(0)
cv2.destroyAllWindows()
