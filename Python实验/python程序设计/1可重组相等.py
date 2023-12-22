t = int(input())

for i in range(0,t):
    s11 = input()
    s22 = input()

    #对字符串排序
    s1 = list(s11)
    s2 = list(s22)
    s1.sort()
    s2.sort()

    if s1==s2:
        print("Yes")
    else:
        print("No")