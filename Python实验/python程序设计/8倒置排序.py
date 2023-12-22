t = int(input())

def rever(a):
    if a == '':
        return a
    else:
        return rever(a[1:]) + a[0]

def intrever(a):
    temp = rever(a)
    return int(temp)

for _ in range(t):
    string = input().split()

    string.remove(string[0])

    string = list(zip(list(map(intrever,string)),string))
    string.sort()
    #print(string)

    for i in range(len(string)):
        if i != len(string)-1:
            print(string[i][1], end=' ')
        else:
            print(string[i][1],end='')
    print()