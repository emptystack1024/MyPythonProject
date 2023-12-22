import random

import cv2
import os
import numpy as np

# 文件夹路径
folder_path = r'Library'


files = os.listdir(folder_path)

# 遍历每个图像文件
for file_name in files:
    full_path = os.path.join(folder_path, file_name)

    # 读取图像
    img_o = cv2.imread(full_path)

    # 图像处理操作（示例，可以根据需求修改）
    # 1. 旋转
    angle = random.randint(0, 360)  # 旋转角度
    rows, cols = img_o.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    img = cv2.warpAffine(img_o, rotation_matrix, (cols, rows))
    img_name = file_name.split('.')[0] + '_xuanzhuan' + '.' + file_name.split('.')[1]
    cv2.imwrite(os.path.join(folder_path, img_name), img)

    # 2. 缩放
    scale_percent = random.randint(50, 150)  # 缩放比例
    width = int(img_o.shape[1] * scale_percent / 100)
    height = int(img_o.shape[0] * scale_percent / 100)
    img = cv2.resize(img_o, (width, height))
    img_name = file_name.split('.')[0] + '_suofang' + '.' + file_name.split('.')[1]
    cv2.imwrite(os.path.join(folder_path, img_name), img)

    # 3. 亮度变化
    brightness_factor = random.randint(50, 250) / 100  # 亮度变化比例
    img = cv2.convertScaleAbs(img_o, alpha=brightness_factor, beta=0)
    img_name = file_name.split('.')[0] + '_liangdu' + '.' + file_name.split('.')[1]
    cv2.imwrite(os.path.join(folder_path, img_name), img)

    # 4. 遮挡（添加一个黑色矩形）
    mask = np.zeros_like(img_o)
    # 随机选择矩形的位置和大小
    start_row = np.random.randint(0, img_o.shape[0] - 20)
    end_row = start_row + np.random.randint(10, 20)
    start_col = np.random.randint(0, img_o.shape[1] - 20)
    end_col = start_col + np.random.randint(10, 20)
    mask[start_row:end_row, start_col:end_col, :] = 255
    img = cv2.add(img_o, mask)

    img_name = file_name.split('.')[0] + '_zhezhang' + '.' + file_name.split('.')[1]
    cv2.imwrite(os.path.join(folder_path, img_name), img)

print("图像处理完成并保存。")
