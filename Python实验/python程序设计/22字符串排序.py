n = int(input())

data = []

for i in range(n):
    data.append(input())

data.sort(key = str)
for i in data:
    print(i)