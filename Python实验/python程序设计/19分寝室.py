m,w,q = map(int,input().split())
#print(m,w,q)

min = 10010
a,b = 0,0
for i in range(1,q):#女生数量
        if m%(q-i)==0 and w%i==0:
            cha = abs((w/i) - (m/(q-i)))
            if cha<min:
                #print(i,(q-i),cha,min)
                b = i
                a = (q-i)
                min = cha

if (a == 0 and b == 0) or min == 10010:
    print("No Solution")
else:
    print(a,b)