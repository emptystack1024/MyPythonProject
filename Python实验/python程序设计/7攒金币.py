t = int(input())

for _ in range(t):
    temp = input()
    temp1 = temp.split(" ")

    sum = 0
    for i in temp1:
        sum += int(i)

    print(sum)