t = int(input())
for _ in range(t):
    date = list(map(int, input().split()))
    n = date[0]
    date = date[1::]
    ans = sorted(date,key = lambda x:(int(str(x)[::-1]),x))
    print(*ans)