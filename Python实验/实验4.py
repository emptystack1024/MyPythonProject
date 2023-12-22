import sys
import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost', user='root', passwd='152822', port=3306,database="world")
print('连接成功！')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS SYSTEM12")

# 使用预处理语句创建表
sql = """CREATE TABLE SYSTEM12 (
        ItemID  INT PRIMARY KEY AUTO_INCREMENT,#主键，唯一，自动增长
        ItemNumber  INT NOT NULL ,#不为空
        xuhao INT,
        ItemString VARCHAR(50) NOT NULL ,#不为空
        UpNumber INT,
        ItemCommand VARCHAR(50) NOT NULL)"""
cursor.execute(sql)
print('建表成功！')

# SQL 插入语句
sql = """INSERT INTO SYSTEM12(ItemNumber,xuhao,ItemString,UpNumber,ItemCommand)
            #菜单项编号是0，从0开始，上一级菜单项id为0，表示没有上一级菜单，选择执行的命令为1，遍历所有父节点是菜单项编号是0的表
            VALUES (1,0,'惠普产品管理系统', 0, '1'),
                            (2,1,'1.售前技术支持', 1, '1'),
                            (3,2,'2.售后服务', 1, '1'),
                            #选择执行的命令是0表示退出系统，1是打印所有UpNUmber为自己的表
                            (0,0,'0.退出系统', 1, '0'),
                            
                            (4,1,'1.产品查询',2,'1'),
                            (5,2,'2.价格查询',2,'1'),
                            (0,3,'3.技术咨询',2,'0'),
                            (0,0,'0.返回上级菜单',2,'-1'),
                            
                            (0,1,'1.产品使用指导',3,'按任意键即可开机'),
                            (0,2,'2.故障报修',3,'本机器是不会有任何故障的'),
                            (0,3,'3.退货办理',3,'本店为黑店，恕不支持退货'),
                            (0,0,'0.返回上级菜单',3,'-1'),
                            
                            (0,1,'1.打印只因',4,'打印只因：超级好用的打印机'),
                            (0,2,'2.扫描仪',4,'扫描仪：超级好用的扫描仪'),
                            (0,3,'3.笔只因本电脑',4,'笔只因本电脑：超级好用的笔只因本电脑'),
                            (0,0,'0.返回上级菜单',4,'-1'),
                            
                            (1,1,'1.打印只因',5,'打印只因：只要99998，把它带回家！'),
                            (2,2,'2.扫描仪',5,'扫描仪：只要99998，把它带回家！'),
                            (3,3,'3.笔只因本电脑',5,'笔只因本电脑：只要99998，把它带回家！'),
                            (0,0,'0.返回上级菜单',5,'-1')"""
# 执行sql语句
cursor.execute(sql)
# 提交到数据库执行
db.commit()
print('插入数据成功！')

# SQL 查询语句
sql = "SELECT * FROM system12"
cursor.execute(sql)
# 获取所有记录列表
results = cursor.fetchall()
print("********************************")
iter = 0
print(results[0][3])
for row in results:
    if(row[4] == 1):
        iter = 1
        print("%s" % \
                (row[3]))
cao = int(input("请输入要操作的序号: "))

while 1:
    for row in results:
        if iter == row[4] and cao == row[2]:
            if(row[5] == '1'):
                iter = row[1]
                for row in results:
                    if (row[4] == iter):
                        print("%s" % \
                              (row[3]))
                cao = int(input("请输入要操作的序号: "))
            elif(row[5] == '0'):
                iter = row[4]
                for row in results:
                    if (row[4] == iter):
                        print("%s" % \
                              (row[3]))
                cao = int(input("请输入要操作的序号: "))
            elif row[5] == '-1':
                print("结束")
                sys.exit()
            else:
                print(row[5])
                sys.exit()

# 关闭数据库连接
db.close()
