_ = int(input())

for i in range(_):

    data = input()
    num = list(data.split(" "))

    lt1 = []
    lt2 = []

    for j in range(int(num[0])):
        lt1.append(int(num[2+j]))

    for j in range(int(num[1])):
        lt2.append(int(num[2+int(num[0])+j]))

    lt1.sort()
    lt2.sort()

    ans = [x for x in lt1 if x not in lt2]
    if len(ans) == 0:
        print("NULL")
    else:
        res = ""
        for i in range(len(ans)):
            if(num != 0):
                res += " "
            res += str(ans[i])
        print(res)