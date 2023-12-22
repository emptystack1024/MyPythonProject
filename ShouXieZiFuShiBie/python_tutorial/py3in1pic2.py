# 一张图解读 Python 基础语法（py3版）
# 来源：Crossin的编程教室
import os

'''
这是多行注释
'''
def main():
    print('Hello World!')

    n = input('你叫什么名字？\n')
    l = input('请输入级别：')
    x = func('Crossin', int(l))
    y = x + 1
    y += 10
    print('score is %s' % y)
    print('=' * 10)
    print('当前目录', os.getcwd())

    food = ['苹果', '桔子', '香蕉', '西瓜']
    counter = {'葡萄': 5}
    num = 0
    for i in food:
        num += 1
        print('我想吃' + i)
        counter[i] = num
    print('计数：', counter)

    for i in range(10):
        print(i, end='，')

    print('\n====while====')
    while True:
        i += 1
        if i > 20:
            break
        print(i, end='、')

    print('\n====write file====')
    text = '；'.join(food)
    with open('output.txt', 'w') as f:
        f.write(text)

    print('main 结束')

def func(name, level=1):
    print("I'm", name)
    print('{} is level {}'.format(name, level))
    l = len(name)
    s = name.find('s')
    if level < 1:
        score = 0
    elif level > 1 and (l > 1 or s > 1):
        score = 100
    else:
        score = 60
    return score

if __name__ == '__main__':
    main()
