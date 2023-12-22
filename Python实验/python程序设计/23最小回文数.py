import math

t = int(input())

if t >= 10:
    for i in range(t,2*t):
        #print(i,int(str(i)[::-1]))
        if i == int(str(i)[::-1]):
            print(i)
            break
else:
    print(t + 1)