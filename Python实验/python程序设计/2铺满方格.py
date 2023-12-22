dp = [0 for i in range(51)]
dp[1] = 1
dp[2] = 2
dp[3] = 4

for i in range(4, 51):
    dp[i] = dp[i-1] + dp[i-2] + dp[i-3]

while True:
    try:
        n = int(input())

        print(dp[n])

    except EOFError:
        break