t = int(input())

stand = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

for _ in range(t):

    string = list(input().split())[1:]

    ans = [i for i in stand if i not in string]
    if len(ans) == 0:
        print("HAHA", end='')
    else:
        print(len(ans),end = ' ')
        for i in range(len(ans)):
            if i != len(ans) - 1:
                print(ans[i], end=' ')
            else:
                print(ans[i], end='')

    if _ != t - 1:
        print()