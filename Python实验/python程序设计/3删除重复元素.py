# t = int(input())
#
# for i in range(t):
#     n = input()
#     dp = n.split(' ')
#     del dp[0]
#
#     temp = list(set(list(dp)))
#     temp.sort()
#
#     s = temp[0]
#     s += ' '
#     for i in range(1,len(temp)):
#         s += temp[i]
#         s += ' '
#
#     print(s[:-1])

t = int(input())

for _ in range(t):
    nums = list(map(int, input().split()))[1:]
    nums = sorted(set(nums))
    print(' '.join(map(str, nums)))