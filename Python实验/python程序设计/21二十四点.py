# 输入游戏解的个数
n = int(input())

# 输出列表
ans = ""

#　循环输入运算符替换并计算结果
for i in range(n):
    if i != 0:
        ans += ' '
    order = input().replace('x','*').replace('/','//')
    try:
        if eval(order) == 24:
            ans += 'Yes'
        else:
            ans += 'No'
    except:
        ans += 'ERROR'
        break

# 输出结果
print(ans)
