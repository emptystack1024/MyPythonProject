import random as rd
from math import sqrt

t = int(input())
def pii(lt):
    coun = 0

    for i in range(len(lt)):
        x,y = lt[i]
        print(x,y)
        if(sqrt((x/100.0)**2+(y/100.0)**2)<=1):
            coun += 1

    return coun

rd.seed(20)  # 设置随机数种子为20
numbers = []
for i in range(t):
    numbers.append([rd.randint(0,100),rd.randint(0, 100)])

print(pii(numbers)/t*4)