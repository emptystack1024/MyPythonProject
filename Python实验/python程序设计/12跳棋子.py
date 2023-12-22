t = int(input())

st = {'angry': -1, 'happy': 1, 'count': 0}


def qia(data):
    for i in data:
        i = min(i, 20)
    return data


for _ in range(t):
    n = int(input())
    data = [10 * n] * 6
    dish = [0] * 6
    # print(data)

    string = input()
    while string != 'finish':
        for i in st:
            im = 0
            if string.find(i) == 0:
                p = st[i]
                temp = list(map(int, list(string.split())[1:]))
                # print(temp)
                # print(len(temp))
                # print(len(data))

                if p == -1:
                    for i in range(len(data)):
                        if (temp[i] > data[i]):
                            print("impossible")
                            im = 1
                            break
                    if im == 1:
                        continue
                    dish = [dish[i] + temp[i] for i in range(len(data))]
                    data = [data[i] - temp[i] for i in range(len(data))]
                    #print('angry')

                elif p == 1:

                    for i in range(len(data)):
                        if (temp[i] > dish[i]):
                            print("impossible")
                            im = 1
                            break
                    if im == 1:
                        continue
                    dish = [dish[i] - temp[i] for i in range(len(data))]
                    data = [data[i] + temp[i] for i in range(len(data))]
                    data = qia(data)
                    #print('happy')

                elif p == 0:
                    print(' '.join(map(str, data)))

        string = input()