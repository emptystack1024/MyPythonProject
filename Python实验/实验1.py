import random

jk = []  # 一副扑克牌
cp = []  # 计算机手中的牌
ps = []  # 人手中的牌
dt = []  # 已经打到桌上的牌

pcp = []  # 显示计算机的牌
pps = []  # 显示人的牌
pdt = []  # 显示桌上的牌

# 人要出的牌的序号

n = 0  # 该谁出牌，0：计算机出牌，1：人出牌
m = 0  # 出牌方式，0首次出牌，1：跟牌
danum = 0 #如果为1，就说明有压的死的牌

def CreateCard():  # 创建一副扑克牌
    weight = [12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    num = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    huase = ['♠', '♥', '♣', '♦']
    for i in range(4):
        for j in range(13):
            jk.append((huase[i], num[j], weight[j]))


def ShuffleCard():  # 洗牌
    t = 0
    while (t != 100000):
        t1 = random.randrange(1, 52)
        t2 = random.randrange(1, 52)
        if (t1 != t2):
            jk[t1], jk[t2] = jk[t2], jk[t1]
            t += 1


def DealCard():  # 发牌
    for i in range(12):
        cp.append(jk.pop())
        ps.append(jk.pop())


def SortCard():  # 整理牌
    cp.sort(key=lambda x: int(x[2]))
    ps.sort(key=lambda x: int(x[2]))


def ShowCard():  # 显示牌
    pcp = [x[0] + x[1] for x in cp]
    pps = [x[0] + x[1] for x in ps]
    pdt = [x[0] + x[1] for x in dt]
    print('计算机手中的牌：', pcp)
    print('人手中的牌：', pps)
    print('桌上的牌：', pdt)


def perCard():  # 为人显示想要输出的牌
    pps = [x[0] + x[1] for x in ps]
    print('人手中的牌：', pps)


def refight():
    n = input('是否再来一局？（y/n）')
    while not(n == 'n' or n == 'no'  or n == 'y' or  n == 'yes'):
        print("输入不符合标准，请输入: n , no , y , yes ")
        n = input('是否再来一局？（y/n）')

    while not(n == 'n' or n == 'no'):
        fight()
        n = input('是否再来一局？（y/n）')

    print('游戏结束')


def fight():
    CreateCard()  # 产生扑克牌
    ShuffleCard()  # 洗牌
    DealCard()  # 发牌
    SortCard()  # 整理牌(按照数字排序)
    ShowCard()  # 显示牌

    n = random.randrange(0, 2)
    m = 0
    danum = 0
    # 该谁出牌，0：人出牌，1：计算机出牌
    # 出牌方式，0首次出牌，1：跟牌


    while len(cp) > 0 and len(ps) > 0:
        if n == 1 and m == 0:
            print('    1:机器首次出牌')
            dt.append(cp.pop(0))
            ShowCard()
            n = 0
            m = 1
        elif n == 0 and m == 0:
            print('    0:人首次出牌')
            perCard()  # 显示人手中的牌
            i = int(input("    你要打出的牌的序号是:"))
            while not(i>0 and i<=len(ps)):
                print("    序号错误，请重新输入")
                i = int(input("    你要打出的牌的序号是:"))
            dt.append(ps.pop(i - 1))

            ShowCard()
            n = 1
            m = 1
        elif n == 1 and m == 1:
            n = 0
            danum = 0
            for i in range(len(cp)):
                if cp[i][2] > dt[-1][2]:
                    print('    机器跟牌')
                    dt.append(cp.pop(i))
                    danum = 1
                    ShowCard()
                    n = 0
                    break

            if danum == 0:
                print("    机器要不起")
                dt.clear()
                m = 0
                n = 0
        elif n == 0 and m == 1:
            print('    人跟牌')
            n = 1
            danum = 0
            for i in range(len(ps)):
                if ps[i][2] > dt[-1][2]:
                    danum = 1
                    break

            if danum == 1:
                perCard()
                i = int(input("    你要打出的牌的序号是:"))

                while not (i > 0 and i <= len(ps) or i == 111 or i == 1111):
                    print("    序号错误，请重新输入")
                    i = int(input("    你要打出的牌的序号是:"))

                if i == 111:
                    print('    要不起')
                    dt.clear()
                    m = 0
                    n = 1
                    continue
                if i == 1111:
                    print('    人类自动认输')
                    break

                if i!=1111 and i!=111:
                    while not(ps[i-1][2] > dt[-1][2]):
                        print("    你的牌没他大，请重新输入")
                        i = int(input("    你要打出的牌的序号是:"))

                dt.append(ps.pop(i - 1))
                ShowCard()
            else:
                print('    要不起')
                dt.clear()
                m = 0

    if len(ps)==0:
        print("    人赢了")
        pcp = [x[0] + x[1] for x in cp]
        print('计算机手中剩余的牌：', pcp)
    else:
        print("    机器赢了")
        pps = [x[0] + x[1] for x in ps]
        print('人手中剩余的牌：', pps)

# 主函数部分
fight()  # 开始游戏
refight()  # 是否再来一局
