n,k = map(int,input().split())

data = list(range(2,n+1))
lt = []
while len(data) != 0:
    p = data[0]
    lt += data[::p]
    #print(lt)
    data = [i for i in data if i not in lt]
    #print(data)

print(lt[k])