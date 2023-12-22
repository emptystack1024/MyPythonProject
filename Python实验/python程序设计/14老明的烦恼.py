from math import inf

_ = int(input())

for i in range(_):
    __ = int(input())
    data = list(map(int,input().split()))
    #print(data)

    temp = input().split()
    while temp[0] != 'End':

        if temp[0] == 'Move':
            #print('Move')
            ii,jj,kk = map(int,temp[1:4])
            #print(ii,jj,kk)
            data[ii-1] -= kk
            data[jj-1] += kk
        elif temp[0] == 'Ask':
            #print('Ask')
            ii, jj = map(int,temp[1:3])
            #print(ii," ",jj)
            lt = data[ii-1:jj]
            #print(lt)
            max = 0
            min = inf
            maxi,mini = 0,0
            for j in range(len(lt)):
                if lt[j]>max:
                    max,maxi = lt[j],j+ii
                if lt[j]<min:
                    min,mini = lt[j],j+ii
            print(mini,maxi)

        #print(data)

        temp = input().split()

    #print('over')