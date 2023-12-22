_ = int(input())

st = {'rock':1,'scissors':2,'paper':3}#1石头2剪刀3布

for i in range(_):
    string = input()
    if i != 0:
        print()

    ite = 0
    aw, bw = 0, 0
    a, b = 0, 0

    while ite < len(string):

        for j in st:
            if(string.find(j, ite) == ite):
                a = st[j]
                #print('a = ',a)
                ite += len(j)
                break

        for j in st:
            if (string.find(j, ite) == ite):
                b = st[j]
                #print('b = ', b)
                ite += len(j)
                break

        if a != b:
            if a == 1:
                if b == 2:
                    aw+=1
                elif b == 3:
                    bw+=1
            elif a == 2:
                if b == 1:
                    bw+=1
                elif b == 3:
                    aw+=1
            elif a == 3:
                if b == 1:
                    aw+=1
                elif b == 2:
                    bw+=1

    if aw > bw:
        print('Win',end="")
    elif aw < bw:
        print('Lose',end="")
    elif aw == bw:
        print('Tie',end="")