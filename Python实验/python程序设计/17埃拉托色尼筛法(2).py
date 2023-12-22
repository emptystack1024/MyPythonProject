def find_number(n, k):
    prime_list = [True] * (n + 1)
    prime_list[0] = prime_list[1] = False
    p = 2
    count = 0
    while (p < n + 1) and (count < k):
        for i in range(p, n + 1, p):
            if prime_list[i]:
                count += 1
                if count == k:
                    return i
                prime_list[i] = False
        p += 1
        while prime_list[p] == False:
            p += 1

n, k = map(int, input().split())
print(find_number(n, k))
