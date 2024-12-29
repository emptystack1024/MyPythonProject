import time
import torch

# 测试gpu计算耗时
A = torch.ones(5000, 5000).to('cuda')
B = torch.ones(5000, 5000).to('cuda')
startTime2 = time.time()
for i in range(100):
    C = torch.matmul(A, B)
endTime2 = time.time()
print('gpu计算总时长:', round((endTime2 - startTime2) * 1000, 2), 'ms')

# 测试cpu计算耗时
A = torch.ones(5000, 5000)
B = torch.ones(5000, 5000)
startTime1 = time.time()
for i in range(100):
    C = torch.matmul(A, B)
endTime1 = time.time()
print('cpu计算总时长:', round((endTime1 - startTime1) * 1000, 2), 'ms')
