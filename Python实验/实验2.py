import pandas as pd

def solve():
    # 读取excel文件
    f = pd.ExcelFile('C:\\code\\pythonProject\\jupy_test\\test.xlsx')

    f_sheet = f.sheet_names
    print(f_sheet)

    area = int(input("你要选择进行转换的单位是哪个序号："))

    while not(area in range(1, len(f_sheet)+1)):
        area = int(input("你输入的区域不存在，请重新输入："))

    print("你选择的区域是：", f_sheet[area-1])

    df = pd.read_excel(f, sheet_name=f_sheet[area-1])
    print(df['单位'].values)

    danwei1 = int(input("你要选择进行转换的单位是哪个序号："))
    while not(danwei1 in range(1, len(df['单位'].values)+1)):
        danwei1 = int(input("你输入的区域不存在，请重新输入："))

    print("你选择的单位是：", df['单位'].values[danwei1-1])

    shuzhi1 = int(input("你要转换的数值是："))
    danwei2 = int(input("你要选择进行转换的单位是哪个序号："))
    while not(danwei2 in range(1, len(df['单位'].values)+1)):
        danwei2 = int(input("你输入的区域不存在，请重新输入："))

    shuzhi2 = shuzhi1 * df['转换系数'].values[danwei2-1] / df['转换系数'].values[danwei1-1]
    print('{0}{1} => {2}{3}'.format(shuzhi1, df['单位'].values[danwei1-1], shuzhi2,df['单位'].values[danwei2-1],))

##主函数部分
solve()
i = input("你还要继续运算吗？（y/n）")
while i == 'y':
    print("*****************************************************")
    solve()
    i = input("你还要继续运算吗？（y/n）")
