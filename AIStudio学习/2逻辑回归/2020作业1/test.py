import pandas as pd
import numpy as np
import math
data = pd.read_csv('./train.csv',encoding = 'big5')
print(data.head())

# 可以看出前三列没有任何意义，在读取数据时应该删除，并且要把数据中的 ’NR‘ 项设置为0
data = data.iloc[:,3:]
data[data == 'NR'] = 0

raw_data = data.to_numpy()

# 每个月份的数据
# 一天有24个小时的数据，一共有18种数据，一个月只记录20天
month_data = {}

for month in range(12):
    temp = np.empty([18,480])
    for day in range(20):
        # temp 记录的是这一天的24项数据
        # raw_data  18*(20*month + day):18*(20*month+day+1)：表示的是每月每天的18条数据
        temp[:,day*24:(day+1)*24] = raw_data[18*(20*month + day):18*(20*month+day+1),:]

    print(temp)
    month_data[month] = temp

# 12个月 乘以  每个月采样471次  为什么是471次？因为前九个小时要做为数据去计算 20*24-9
# 18种数据 乘以 前9个小时的数据
x = np.empty([12*471,18*9],dtype=float)
y = np.empty([12*471,1],dtype=float)

for month in range(12):
    for day in range(20):
        for hour in range(24):
            if day == 19 and hour > 14: # 最后一天的时候，最后面是没有y的，滑动窗口会有问题
                continue

            x[month*471 + day*24 + hour,:] = month_data[month][:,day*24 + hour : day*24 + hour + 9].reshape(1,-1)
            y[month*471 + day*24 + hour,0] = month_data[month][9,day*24 + hour + 9]

# 对所有的数据进行标准化
mean_x = np.mean(x,axis = 0)
std_x = np.std(x,axis = 0)

for i in range(len(x)):
    for j in range(len(x[0])):
        if std_x[j] != 0:
            x[i][j] = (x[i][j] - mean_x[j]) / std_x[j]

x_train_set = x[:math.floor(len(x) * 0.8),:]
y_train_set = y[:math.floor(len(x) * 0.8),:]

x_validation = x[math.floor(len(x) * 0.8):,:]
y_validation = y[math.floor(len(x) * 0.8):,:]

dim = 18 * 9 + 1 # 加1是为了偏置项
w = np.zeros([dim,1])

learning_rate = 0.1
iter_time = 50000

adagrad = np.zeros([dim,1])
eps = 0.0001
w = np.zeros([dim, 1])
Input = np.concatenate((np.ones([x_train_set.shape[0], 1]), x_train_set), axis=1).astype(float)

for t in range(iter_time):
    # 计算损失
    loss = np.sqrt(np.sum(np.power(np.dot(Input, w) - y_train_set, 2)))

    # 打印损失
    if t % 1000 == 0:
        print(f"迭代次数：{t}   损失值：{loss}")

    # 计算梯度
    gradient = 2 * np.dot(Input.transpose(), np.dot(Input, w) - y_train_set)

    # 更新adagrad
    adagrad += np.power(gradient, 2)

    # 更新权重
    w = w - (learning_rate / np.sqrt(adagrad + eps)) * gradient

# 保存训练后的权重
np.save('./weight.npy', w)


from matplotlib import pyplot as plt
weights = np.load('./weight.npy')

x_axis = np.arange(y_validation.shape[0])
x_validation_input = np.concatenate((np.ones([x_validation.shape[0], 1]), x_validation), axis = 1).astype(float)
ans_y = np.dot(x_validation_input,weights)

# 保存为csv文件，并提交到kaggle：https://www.kaggle.com/c/ml2020spring-hw1/submissions
import csv
with open('submit.csv', mode='w', newline='') as submit_file:
    csv_writer = csv.writer(submit_file)
    header = ['id', 'value']
    print(header)
    csv_writer.writerow(header)
    for i in range(240):
        row = ['id_' + str(i), ans_y[i][0]]
        csv_writer.writerow(row)