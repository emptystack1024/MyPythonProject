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

    集合1 = set(lt1)
    集合2 = set(lt2)

    答案 = 集合1 - 集合2

    if(len(答案) == 0):
        print("NULL")
    else:
        for i in 答案:
            print(i,end=' ')
        print()