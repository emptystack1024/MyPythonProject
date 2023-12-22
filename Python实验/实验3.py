print("请选择要进行的模式: ")
a = int(input("1.读取本地文件code.txt    2.输入代码并将代码存入test.txt \n"))
while not(a == 1 or a == 2):
    print("输入序号错误，请重新输入")
    a = int(input("1.读取本地文件code.txt    2.输入代码并将代码存入test.txt \n"))

if a==1:
    f1 = open('code.txt','r',encoding='utf-8')
    code = f1.read()
    f1.close()

    print(code)

elif a ==2:
    f4 = open('test.txt','w',encoding='utf-8')
    print("请输入要转换的代码（用quit表示结束输入）：")

    code = ""
    while True:
        strs = input()
        if strs != "quit":
            code += '\n'
            code += strs
        else:
            break

    print("这是你写入的代码：")
    print(code)

    f4.write(code)
    f4.close()

f2 = open('final.txt','w',encoding='utf-8')


print("************************************************************")
status = 0 #1-预备注释 2-单行注释 3-多行注释 4-预备取消注释
sy = 0 #如果sy = 1表示代码处于字符串状态，不进行程序上的判断

for char in code:
    if char == '"' and sy == 0:
        print("进入字符串状态")
        sy = 1
    elif char == '"' and sy == 1:
        print("退出字符串状态")
        sy = 0

    if sy == 0:
        if status == 0:
            if char == '/':
                status = 1
                print("检测到第一个/")
            else:
                f2.write(char)

        elif status == 1: #进入预备注释状态
            if char == '/':
                status = 2
                print("进入判断单行注释结束状态")
            elif char == '*':
                status = 3
                print("进入判断多行注释结束状态")
            else:
                status = 0 #
                print('退出预备注释状态')
                f2.write('/')
                print("")
                f2.write(char)

        elif status == 2:
            if char == '\n':
                print(r"检测到 \n ，单行注释状态结束")
                status = 0
                f2.write(char)

        elif status == 3:
            if char == '*':
                print("检测到多行注释 结尾处的 * ")
                status = 4

        elif status == 4:
            if char == '/':
                print("检测到多行注释 结尾处的 / ")
                print("多行注释状态结束")
                status=0
            else:
                if char!='*':
                    status = 3
    else:
        f2.write(char)

f2.close()
print("************************************************************")
print("显示转换后的结果：")
f3 = open('final.txt','r',encoding='utf-8')
code = f3.read()
print(code)
f3.close()