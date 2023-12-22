from datetime import datetime

T = int(input())
for _ in range(T):
    d1, d2 = input().split()
    date1 = datetime.strptime(d1, '%Y-%m-%d')
    date2 = datetime.strptime(d2, '%Y-%m-%d')
    delta = date2 - date1
    print(delta.days)