#编写一个函数printName()，打印当前模块的_name_属性的值，主函数中调用该函数，程序保存为nametest.py文件。

#new_nametest.py
#coding=utf-8

def printName():
    print("模块名为：" + __name__)

#主函数
if __name__ == '_main_':
    printName()