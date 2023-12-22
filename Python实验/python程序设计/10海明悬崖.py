t = int(input())

for _ in range(t):
    x = input().split()
    y = bin(int(x[1]))
    x = bin(int(x[0]))
    #print(x,y)

    if len(x)>len(y):
        y = '0b' + '0'*(len(x)-len(y)) + y[2:]
    elif len(y)>len(x):
        x = '0b' + '0'*(len(y)-len(x)) + x[2:]

    #print(x,y)

    count = 0
    for i in range(len(x)):
        if(x[i] != y[i]):
            count += 1

    if count == len(x)-2:
        print("Yes")
    else:
        print("No")