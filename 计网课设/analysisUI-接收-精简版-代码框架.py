from tkinter.ttk import Combobox

from scapy.all import *
from tkinter import *
import tkinter as tk
import time, threading
import tkinter.messagebox as messagebox
import struct

from scapy.layers.dns import DNS
from scapy.layers.inet import IP, ICMP, TCP, in4_chksum, UDP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import Ether, ARP

# 实现进制转换
def decimal_to_four_bit_binary(decimal_num):
    # 将十进制数转换为二进制数，并去掉前缀"0b"
    binary_num = bin(decimal_num)[2:]

    # 确保二进制数是四位数
    while len(binary_num) < 4:
        binary_num = '0' + binary_num

    return binary_num

def IP_headchecksum(IP_head):
    checksum =0
    headlen = len(IP_head)
    if headlen % 2 == 1:
        IP_head += b"\0"
    i=0
    while i<headlen:
        temp = struct.unpack('!H',IP_head[i:i+2])[0]
        checksum = checksum+temp
        i=i+2
    #捋高16bit与低16bit相加
    checksum = (checksum>>16)+(checksum&0xffff)
    #丹进位到高位的16b1t与低16b1t再相加
    checksum = checksum+(checksum>>16)
    return ~checksum & 0xffff

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        #  存储抓包数据
        self.sniffDataList = []
        self.createWidgets() # 创建UI界面

        self.sniffFlag = True  # 设置控制捕获线程运行的标志变量

    def createWidgets(self):
        self.geometry('600x800')
        self.title('协议分析器')

        self.count = 0  # 记录捕获数据帧的个数
        self.countAct = 0 #实际捕获数据帧的个数

        # 创建并添加协议分析器控制组件及面板
        self.createControlWidgets()
        # 创建并添加协议分析主面板
        self.mainPDUShowWindow = PanedWindow(self, orient=tk.VERTICAL, sashrelief=RAISED, sashwidth=5)

        '''
        创建并添加协议分析各动态窗口，包括：
            协议摘要信息窗口PDUSumPanedWindow
            协议详细解析窗口PDUAnalysisPanedWindow
            协议报文编码窗口PDUCodePanedWindow
        '''
        self.createPDUSumPanedWindow()
        self.createPDUAnalysisPanedWindow()
        self.createPDUCodePanedWindow()
        self.mainPDUShowWindow.pack(fill=BOTH, expand=1)

    def createControlWidgets(self):
        # 创建控制面板
        controlFrame = Frame()
        self.countLabel = Label(controlFrame, text='请输入待捕获的数据帧数：')
        self.countLabel.pack()

        countvar = StringVar(value='0')
        self.countInput = Entry(controlFrame, textvariable=countvar, width=6)
        self.countInput.pack()

        self.conditionLabel = Label(controlFrame, text='请输入捕获条件：')
        self.conditionLabel.pack()

        self.conditionInput = Entry(controlFrame, width=60)
        self.conditionInput.pack()

        # 在创建控制面板设置startListenButton按键
        self.startListenButton = Button(controlFrame, text='开始捕获', command=self.start_sniff)
        self.startListenButton.pack()

        # 在创建控制面板放置clearButton按钮
        self.clearButton = Button(controlFrame, text='清空数据', command=self.clearData)
        self.clearButton.pack()

        # 在创建控制面板放置stopListenButton按钮
        self.stopListenButoon = Button(controlFrame, text='停止捕获', command=self.stop_sniff)
        self.stopListenButoon.pack()

        # 实时更新捕获数据帧个数
        self.CountNum = Label(controlFrame, text=("已捕获数据帧个数：" + str(len(self.sniffDataList))))
        self.CountNum.pack()
        # 刷新
        self.refresh()

        controlFrame.pack(side=TOP, fill=Y)

    # 实现一直刷新
    def refresh(self):
        self.CountNum.config(text=("已捕获数据帧个数：" + str(len(self.sniffDataList))))
        self.after(1, self.refresh)

    # 创建显示捕获报文的摘要的窗口
    def createPDUSumPanedWindow(self):
        # 实现一个框架和水平，垂直滑动条
        PDUSumFrame = Frame()
        yScroll = Scrollbar(PDUSumFrame, orient=VERTICAL)
        xScroll = Scrollbar(PDUSumFrame, orient=HORIZONTAL)

        # 创建列表框显示捕获报文的摘要
        self.listbox = tk.Listbox(PDUSumFrame,
                                  xscrollcommand=xScroll.set,
                                  yscrollcommand=yScroll.set)
        xScroll['command'] = self.listbox.xview
        yScroll['command'] = self.listbox.yview

        # 显示波动条
        yScroll.pack(side=RIGHT, fill=Y)
        xScroll.pack(side=BOTTOM, fill=X)

        # 关联用户选择报文进行详细解析的事件
        self.listbox.bind('<Double-ButtonPress>', self.choosedPDUAnalysis)
        self.listbox.pack(fill=BOTH)
        PDUSumFrame.pack(fill=BOTH)
        self.mainPDUShowWindow.add(PDUSumFrame)

    # 创建显示捕获报文分层解析的窗口
    def createPDUAnalysisPanedWindow(self):
        PDUAnalysisFrame = Frame()
        self.PDUAnalysisText = Text(PDUAnalysisFrame)

        # 添加滚动条
        s1 = Scrollbar(PDUAnalysisFrame, orient=VERTICAL)
        s1.pack(side=RIGHT, fill=Y)
        s1.config(command=self.PDUAnalysisText.yview)
        self.PDUAnalysisText['yscrollcommand'] = s1.set

        # 显示组件
        self.PDUAnalysisText.pack(fill=BOTH)
        self.mainPDUShowWindow.add(PDUAnalysisFrame)

    # 创建显示捕获报文原始编码信息的窗口
    def createPDUCodePanedWindow(self):
        # 创建显示捕获数据的窗口
        PDUCodeFrame = Frame()

        # 创建显示捕获数据的文本框
        self.PDUCodeText = Text(PDUCodeFrame)

        # 创建一个纵向滚动的滚动条，铺满Y方向
        s1 = Scrollbar(PDUCodeFrame, orient=VERTICAL)
        s1.pack(side=RIGHT, fill=Y)
        s1.config(command=self.PDUCodeText.yview)
        self.PDUCodeText['yscrollcommand'] = s1.set

        # 显示组件
        self.PDUCodeText.pack(fill=BOTH)
        PDUCodeFrame.pack(side=BOTTOM, fill=BOTH)
        self.mainPDUShowWindow.add(PDUCodeFrame)



    # 启动捕获线程
    def start_sniff(self):
        if self.sniffFlag is True:
            answer = messagebox.askyesnocancel(title='确认窗口', message="是否开始报文捕获？")
            if answer is False:
                print("停止报文捕获！")
                return
            elif answer is True:
                print("开始新的报文捕获！")
                self.startListenButton["state"] = 'disabled'
                self.stopListenButoon["state"] = 'normal'
                self.sniffFlag = False
                if self.startListenButton['text'] == '开始捕获':
                    t = threading.Thread(target=self.PDU_sniff, name='LoopThread')
                    t.start()
                    print(threading.current_thread().name+' 1') # https://blog.csdn.net/briblue/article/details/85101144

    def PDU_sniff(self):
        self.count=int(self.countInput.get())
        if self.count==0:
            self.count=float('inf') #无穷

        # sniff(filter='arp or ip or ip6 or tcp or udp',
        # prn=(lambda x: self.ip_monitor_callback(x)),
        # stop_filter=(lambda x: self.sniffFlag), store=0, iface='WLAN')
        # 指定无线网卡 一定要加filter='arp or ip or ip6 or tcp or udp'参数，协议名称一定要小写，
        # 否则无法顺利抓包 (filter BPF过滤规则 BPF：柏克莱封包过滤器（Berkeley Packet Filter，缩写BPF），
        # 是类Unix系统上数据链路层的一种原始接口，提供原始链路层封包的收发。) 回调函数：一个高层调用底层，
        # 底层再回过头来调用高层的过程。Scapy Sniffer的filter语法：https://blog.csdn.net/qwertyupoiuytr/a
        # rticle/details/54670477 有时候TCP和UDP校验和会由网卡计算(https://blog.csdn.net/weixin_34308389/
        # article/details/93114074)，因此wireshark抓到的本机发送的TCP/UDP数据包的校验和都是错误的，这样检验
        # 校验和根本没有意义。所以Wireshark不自动做TCP和UDP校验和的校验。如果要校验校验和：可以在edit->prefer
        # ence->protocols中选择相应的TCP或者UDP协议，在相应的地方打钩。Scapy之sniff函数抓包参数详解：https:/
        # /www.cnblogs.com/cheuhxg/p/15043117.html

        sniff(filter="arp or ip or ip6 or tcp or udp", prn=(lambda x: self.ip_monitor_callback(x)), stop_filter=(lambda x: self.sniffFlag), store=0)
        # iface=None 则代表所有网卡 filter="arp or ip or ip6 or tcp or udp" 可选值：ether, fddi, tr, wlan, ip, ip6, arp, rarp, decnet, tcp, udp,
        # icmp (fddi, tr, wlan是ether的别名, 包结构很类似) https://www.cnblogs.com/cheuhxg/p/15043117.html

        # sniff(prn=self.ip_monitor_callback, stop_filter=self.sniffFlag, store=0)
        # Scapy之sniff函数抓包参数详解：https://www.cnblogs.com/cheuhxg/p/15043117.html

    # 停止捕获线程
    def stop_sniff(self):
        self.startListenButton["state"] = 'normal'
        self.stopListenButoon["state"] = 'disable'
        self.sniffFlag = True

        self.count = 0
        self.countAct = 0

    # 清空捕获数据
    def clearData(self):
        if self.sniffFlag is True:
            self.listbox.delete(0, END)
            self.sniffDataList = []
            self.PDUAnalysisText.delete(1.0, END)
            self.PDUCodeText.delete(1.0, END)
            self.count = 0
            self.countAct=0
        else:
            messagebox.showinfo(title='友情提示', message="请先停止捕获！！")

    # 分割条件的函数
    def split_condition(self):
        conditionString = self.conditionInput.get()
        splitList = conditionString.split(' ')
        splitStrings = []
        for conString in splitList:
            splitStrings.append(conString)
        return splitStrings

    def split_dulequal(self, dul):  # 按照等号划分后获得筛选的条件
        splitList = dul.split('==')
        return splitList[1]

    #回调函数，根据筛选条件调用不同的分析函数
    def ip_monitor_callback(self, pkt):
        print(pkt.show())
        pktSummaryInfo = str(self.countAct) + ' ' + pkt.summary()
        if self.conditionInput.get().find('IP') != -1:
            src_IP = ''
            dst_IP = ''
            proto_IP = ''
            if pkt.haslayer('IP') and self.countAct < self.count:
                split_condition = self.split_condition()
                for split_con in split_condition:
                    if split_con.find('src') != -1:
                        src_IP = self.split_dulequal(split_con)
                    if split_con.find('dst') != -1:
                        dst_IP = self.split_dulequal(split_con)
                    if split_con.find('proto') != -1:
                        proto_IP = int(self.split_dulequal(split_con))
                if src_IP != '' and dst_IP != '' and proto_IP != '':
                    if pkt['IP'].src == src_IP and pkt['IP'].dst == dst_IP and pkt['IP'].proto == proto_IP:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct+=1
                if src_IP != '' and dst_IP != '' and proto_IP == '':
                    if pkt['IP'].src == src_IP and pkt['IP'].dst == dst_IP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_IP != '' and dst_IP == '' and proto_IP != '':
                    if pkt['IP'].src == src_IP and pkt['IP'].proto == proto_IP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_IP == '' and dst_IP != '' and proto_IP != '':
                    if pkt['IP'].dst == dst_IP and pkt['IP'].proto == proto_IP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_IP != '' and dst_IP == '' and proto_IP == '':
                    if pkt['IP'].src == src_IP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_IP == '' and dst_IP == '' and proto_IP != '':
                    if pkt['IP'].proto == proto_IP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_IP == '' and dst_IP != '' and proto_IP == '':
                    if pkt['IP'].dst == dst_IP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_IP == '' and dst_IP == '' and proto_IP == '':
                    self.sniffDataList.append(pkt)
                    self.listbox.insert(END, pktSummaryInfo)
                    self.countAct += 1
            if self.countAct==self.count:
                self.stop_sniff()

        elif self.conditionInput.get().find('ARP') != -1:
            hwsrc_ARP = ''
            hwdst_ARP = ''
            psrc_ARP = ''
            pdst_ARP = ''
            op_ARP = ''
            if pkt.haslayer('ARP') and self.countAct < self.count:
                split_condition = self.split_condition()
                for split_con in split_condition:
                    if split_con.find('hwsrc') != -1:
                        hwsrc_ARP = self.split_dulequal(split_con)
                    if split_con.find('hwdst') != -1:
                        hwdst_ARP = self.split_dulequal(split_con)
                    if split_con.find('psrc') != -1:
                        psrc_ARP = self.split_dulequal(split_con)
                    if split_con.find('pdst') != -1:
                        pdst_ARP = self.split_dulequal(split_con)
                    if split_con.find('op') != -1:
                        op_ARP = self.split_dulequal(split_con)
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt[
                        'ARP'].psrc == psrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt[
                        'ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt[
                        'ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].psrc == psrc_ARP and pkt[
                        'ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].psrc == psrc_ARP and pkt[
                        'ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].psrc == psrc_ARP and \
                            pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].psrc == psrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].psrc == psrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].psrc == psrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwsrc == hwsrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].hwdst == hwdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].hwdst == hwdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].op == op_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].hwdst == hwdst_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP != '':
                    if pkt['ARP'].psrc == psrc_ARP and pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP != '':
                    if pkt['ARP'].pdst == pdst_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP != '' and pdst_ARP == '':
                    if pkt['ARP'].psrc == psrc_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP != '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].hwdst == hwdst_ARP:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP != '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].hwsrc == hwsrc_ARP:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP != '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP == '':
                    if pkt['ARP'].op == op_ARP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if op_ARP == '' and hwsrc_ARP == '' and hwdst_ARP == '' and psrc_ARP == '' and pdst_ARP == '':
                    self.sniffDataList.append(pkt)
                    self.listbox.insert(END, pktSummaryInfo)
                    self.countAct += 1
            if self.countAct==self.count:
                self.stop_sniff()

        elif self.conditionInput.get().find('Ether') != -1:
            src_Ether = ''
            dst_Ether = ''
            if pkt.haslayer('Ether') and self.countAct < self.count:
                split_condition = self.split_condition()
                for split_con in split_condition:
                    if split_con.find('src') != -1:
                        src_Ether = self.split_dulequal(split_con)
                    if split_con.find('dst') != -1:
                        dst_Ether = self.split_dulequal(split_con)
                if src_Ether != '' and dst_Ether != '':
                    if pkt['Ether'].src == src_Ether and pkt['Ether'].dst == dst_Ether:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_Ether != '' and dst_Ether == '':
                    if pkt['Ether'].src == src_Ether:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_Ether == '' and dst_Ether != '':
                    if pkt['Ether'].dst == dst_Ether:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if src_Ether == '' and dst_Ether == '':
                    self.sniffDataList.append(pkt)
                    self.listbox.insert(END, pktSummaryInfo)
                    self.countAct += 1
            if self.countAct == self.count:
                self.stop_sniff()

        elif self.conditionInput.get().find('TCP') != -1:
            sport_TCP = ''
            dport_TCP = ''
            if pkt.haslayer('TCP') and self.countAct < self.count:
                split_condition = self.split_condition()
                for split_con in split_condition:
                    if split_con.find('sport') != -1:
                        sport_TCP = int(self.split_dulequal(split_con))
                    if split_con.find('dport') != -1:
                        dport_TCP = int(self.split_dulequal(split_con))
                if sport_TCP != '' and dport_TCP != '':
                    if pkt['TCP'].sport == sport_TCP and pkt['TCP'].dport == dport_TCP:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if sport_TCP != '' and dport_TCP == '':
                    if pkt['TCP'].sport == sport_TCP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if sport_TCP == '' and dport_TCP != '':
                    if pkt['TCP'].dport == dport_TCP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if sport_TCP == '' and dport_TCP == '':
                    self.sniffDataList.append(pkt)
                    self.listbox.insert(END, pktSummaryInfo)
                    self.countAct += 1
            if self.countAct == self.count:
                    self.stop_sniff()

        elif self.conditionInput.get().find('UDP') != -1:
            sport_UDP = ''
            dport_UDP = ''
            if pkt.haslayer('UDP') and self.countAct < self.count:
                split_condition = self.split_condition()
                for split_con in split_condition:
                    if split_con.find('sport') != -1:
                        sport_UDP = int(self.split_dulequal(split_con))
                    if split_con.find('dport') != -1:
                        dport_UDP = int(self.split_dulequal(split_con))
                if sport_UDP != '' and dport_UDP != '':
                    if pkt['UDP'].sport == sport_UDP and pkt['UDP'].dport == dport_UDP:
                        self.sniffDataList.append(pkt)  # 把sniff函数抓到的数据包加入到捕获队列里
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if sport_UDP != '' and dport_UDP == '':
                    if pkt['UDP'].sport == sport_UDP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if sport_UDP == '' and dport_UDP != '':
                    if pkt['UDP'].dport == dport_UDP:
                        self.sniffDataList.append(pkt)
                        self.listbox.insert(END, pktSummaryInfo)
                        self.countAct += 1
                if sport_UDP == '' and dport_UDP == '':
                    self.sniffDataList.append(pkt)
                    self.listbox.insert(END, pktSummaryInfo)
                    self.countAct += 1
            if self.countAct == self.count:
                    self.stop_sniff()

        else:
            if self.count>self.countAct:
                self.countAct += 1
                self.sniffDataList.append(pkt)
                self.listbox.insert(END, pktSummaryInfo)

        print(threading.current_thread().name+' 2') # https://blog.csdn.net/briblue/article/details/85101144
        # time.sleep(1) # 最好不要延时，否则好多包抓不到

    def IP_headchecksum(self, IP_head):
        checksum = 0
        headlen = len(IP_head)
        if headlen % 2 == 1:
            # b:signed type
            IP_head += b"\0"
        i = 0
        while i < headlen:
            temp = struct.unpack('!H', IP_head[i:i + 2])[0]
            checksum = checksum + temp
            i = i + 2
        # 将高16bit与低16bit相加
        checksum = (checksum >> 16) + (checksum & 0xffff)
        # 将高16bit与低16bit再相加
        checksum = checksum + (checksum >> 16)
        return ~checksum & 0xffff

    def proto_IPcol(self, ori_protocol):
        if ori_protocol == 1:
            proString = 'ICMP'
        elif ori_protocol == 6:
            proString = 'TCP'
        elif ori_protocol == 17:
            proString = 'UDP'
        elif ori_protocol == 89:
            proString = 'OSPF'
        elif ori_protocol == 0:
            proString = 'IPv6 Hop-by-Hop Option'
        elif ori_protocol == 58:
            proString = 'ICMPv6'
        elif ori_protocol == 4:
            proString = 'IP'
        return proString

    #对应进制转换
    def intbin(self, n, count):
        """returns the binary of integer n, using count number of digits"""
        return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])

    def choosedPDUAnalysis(self, event):
        choosePDUNum = self.listbox.curselection()[0]
        choosedPacket = self.sniffDataList[choosePDUNum]
        if self.conditionInput.get().find('IP') != -1:
            self.choosedIPPDUAnalysis()
        elif self.conditionInput.get().find('ARP') != -1:
            self.choosedARPPDUAnalysis()
        elif self.conditionInput.get().find('Ether') != -1: # 以太网MAC协议
            self.choosedEtherPDUAnalysis()
        elif self.conditionInput.get().find('TCP') != -1:
            self.choosedTCPPDUAnalysis()
        elif self.conditionInput.get().find('UDP') != -1:
            self.choosedUDPPDUAnalysis()
        elif self.conditionInput.get() == '':
            if choosedPacket.haslayer('IP'):
                self.choosedIPPDUAnalysis()
            elif choosedPacket.haslayer('ARP'):
                self.choosedARPPDUAnalysis()
            elif choosedPacket.haslayer('Ether'): # 以太网MAC协议
                self.choosedEtherPDUAnalysis()
            elif choosedPacket.haslayer('TCP'):
                self.choosedTCPPDUAnalysis()
            elif choosedPacket.haslayer('UDP'):
                self.choosedUDPPDUAnalysis()

    def choosedEtherPDUAnalysis(self):
        # 请在此处完成MAC协议的分析器(分析数据包功能)，并添加详细代码注释
        choosePDUNum = self.listbox.curselection()[0]
        choosedPacket = self.sniffDataList[choosePDUNum]

        # 实现对文本框内的文字进行删除，然后重新打印IP信息
        self.PDUAnalysisText.delete("1.0", END)

        # 打印Ether信息---------------------------------------------------------------------
        Ethertext = ("Ether Ⅱ, Src: " + choosedPacket['Ethernet'].src + ", Dst: " + choosedPacket['Ethernet'].dst + "\n")
        Ethertext += ("     Destination: " + choosedPacket['Ethernet'].dst + "\n")
        Ethertext += ("     Source: " + choosedPacket['Ethernet'].src + "\n")
        Ethertext += ("     Type: " + str(choosedPacket['Ethernet'].type) + "\n")
        Ethertext += ("     payload: " + str(raw(choosedPacket['Ethernet'].payload)) + "\n")

        self.PDUAnalysisText.insert(END, Ethertext)

        # 打印原始报文---------------------------------------------------------------------
        self.PDUCodeText.delete("1.0", END)
        # 创建一个StringIO对象，用于捕获hexdump的输出
        output = io.StringIO()
        sys.stdout = output  # 将stdout重定向到StringIO对象

        # 将原始报文输入到控制台
        hexdump(choosedPacket)

        # 从StringIO对象中获取hexdump的输出字符串
        EtherBaowen = output.getvalue()

        # 恢复stdout的原始设置
        sys.stdout = sys.__stdout__

        self.PDUCodeText.insert(END, EtherBaowen)

    def tcpflag(self, tcpflag):  # 将标志位是1的拼接
        flagString = ' '
        flag = 0
        if tcpflag & 0x80:
            if flag == 0:
                flagString += 'CWR'
                flag = 1
            else:
                flagString += ',CWR'
        if tcpflag & 0x40:
            if flag == 0:
                flagString += 'ECE'
                flag = 1
            else:
                flagString += ',ECE'
        if tcpflag & 0x20:
            if flag == 0:
                flagString += 'URG'
                flag = 1
            else:
                flagString += ',URG'
        if tcpflag & 0x10:
            if flag == 0:
                flagString += 'ACK'
                flag = 1
            else:
                flagString += ',ACK'
        if tcpflag & 0x08:
            if flag == 0:
                flagString += 'PSH'
                flag = 1
            else:
                flagString += ',PSH'
        if tcpflag & 0x04:
            if flag == 0:
                flagString += 'RST'
                flag = 1
            else:
                flagString += ',RST'
        if tcpflag & 0x02:
            if flag == 0:
                flagString += 'SYN'
                flag = 1
            else:
                flagString += ',SYN'
        if tcpflag & 0x01:
            if flag == 0:
                flagString += 'FIN'
                flag = 1
            else:
                flagString += ',FIN'
        return flagString

    def addEther(self, Ether):
        text = ""
        text += ("Ether Ⅱ, Src: " + Ether.src + ", Dst: " + Ether.dst + "\n")
        text += ("     Destination: " + Ether.dst + "\n")
        text += ("     Source: " + Ether.src + "\n")
        text += ("     Type: " + str(Ether.type) + "\n")
        return text

    def addIP(self, IPs):
        tcp_Flag =IPs.flags
        flagTrans = self.tcpflag(tcp_Flag)

        text = ""
        text += ("Internet Protocol Version 4, Src: " + IPs.src + ", Dst: " + IPs.dst + "\n")
        text += ("     " + decimal_to_four_bit_binary(IPs.version) + " .... = Version: " + str(IPs.version) + "\n")
        text += ("     .... " + decimal_to_four_bit_binary(IPs.ihl) + " = Header Length: " + str(IPs.ihl) + "\n")
        text += ("     Differentiated Services Field: 0x" + decimal_to_four_bit_binary(IPs.tos) + "\n")
        text += ("     Total Length: " + str(IPs.len) + "\n")
        text += ("     Identification: 0x" + decimal_to_four_bit_binary(IPs.id) + "(" + str(IPs.id) + ")" + "\n")
        text += ("     Flags: 0x%03x " % int(IPs.flags) + "(" + flagTrans + ")" + "\n")
        text += ("            0... .... .... = Reserved: Not set" + "\n")
        if IPs.flags.DF == 0:
            text += ("            .0.. .... .... = Don't fragment: Not set" + "\n")
        else:
            text += ("            .1.. .... .... = Don't fragment: Set" + "\n")
        if IPs.flags.MF == 0:
            text += ("            ..0. .... .... = More fragments: Not set" + "\n")
        else:
            text += ("            ..1. .... .... = More fragments: Set" + "\n")
        text += ("     Fragment offset: " + str(IPs.frag) + "\n")
        text += ("     Time to live: " + str(IPs.ttl) + "\n")
        text += ("     Protocol: " + str(IPs.proto) + "\n")

        # 计算校验和
        ip_packet = IPs
        x = raw(ip_packet)
        ipraw = IP(x)
        checksum_scapy = ipraw[IP].chksum
        text += ("     Header checksum: " + hex(checksum_scapy) + " [correct]\n")

        ip_packet.chksum = 0
        x = raw(ip_packet)
        ipString = "".join("%02x" % orb(x) for x in x)
        ipbytes = bytearray.fromhex(ipString)
        checksum_IP = self.IP_headchecksum(ipbytes[0:20])

        if checksum_scapy == checksum_IP:
            text += ("""     [Header checksum status: Good]-++++++++""" + "\n")
        else:
            text += ("""     [Header checksum status: Bad]""" + "\n")
        text += ("     [Calculated checksum: " + hex(checksum_IP) + "]\n")

        text += ("     Source: " + str(IPs.src) + "\n")
        text += ("     Destination: " + str(IPs.dst) + "\n")

        return text

    def addARP(self,ARPs):
        text = ""
        # 判断是请求还是回复
        if ARPs.op == 1:
            text += ("Address Resolution Protocol (request)" + "\n")
        else:
            text += ("Address Resolution Protocol (reply)" + "\n")
        text += ("     Hardware type: " + str(ARPs.hwtype) + "\n")
        text += ("     Protocol type: " + str(ARPs.ptype) + "\n")
        text += ("     Hardware size: " + str(ARPs.hwlen) + "\n")
        text += ("     Protocol size: " + str(ARPs.plen) + "\n")

        if ARPs.op == 1:
            text += ("     Opcode ： request(" + str(ARPs.op) + ")\n")
        else:
            text += ("     Opcode ： reply(" + str(ARPs.op) + ")\n")
        text += ("     Sender MAC address: " + ARPs.hwsrc + "\n")
        text += ("     Sender IP address: " + ARPs.psrc + "\n")
        text += ("     Target MAC address: " + ARPs.hwdst + "\n")
        text += ("     Target IP address: " + ARPs.pdst + "\n")

        return text

    def addTCP(self, TCPs, IPs):
        text = ""

        tcp_Flag = TCPs.flags
        flagTrans = self.tcpflag(tcp_Flag)

        text += ("Transmission Control Protocol, Src Port: " + str(TCPs.sport) + ", Dst Port: " + str(
            TCPs.dport) + ", Seq: " + str(TCPs.seq) + ", Ack: " + str(TCPs.ack) + "\n")
        text += ("     Source Port: " + str(TCPs.sport) + "\n")
        text += ("     Destination Port: " + str(TCPs.dport) + "\n")
        text += ("     Sequence number: " + str(TCPs.seq) + "\n")
        text += ("     Acknowledgment number: " + str(TCPs.ack) + "\n")
        text += ("     " + str(decimal_to_four_bit_binary(TCPs.dataofs)) + " .... = Header Length: " + str(
            TCPs.dataofs) + " bytes (" + str(TCPs.dataofs * 4) + ")\n")
        text += ("     Flags: 0x%03x " % int(TCPs.flags) + "(" + flagTrans + ")" + "\n")

        text += ("            000. .... .... = Reserved: Not set" + "\n")
        text += ("            ...0 .... .... = More fragments: Not set" + "\n")

        if TCPs.flags.CWR == 0:
            text += ("            .... 0... .... = Congestion Window Reduced (CWR): Not set" + "\n")
        else:
            text += ("            .... 1... .... = Congestion Window Reduced (CWR): Set" + "\n")
        if TCPs.flags.ECE == 0:
            text += ("            .... .0.. .... = ECN-Echo: Not set" + "\n")
        else:
            text += ("            .... .1.. .... = ECN-Echo: Set" + "\n")
        if TCPs.flags.URG == 0:
            text += ("            .... ..0. .... = Urgent: Not set" + "\n")
        else:
            text += ("            .... ..1. .... = Urgent: Set" + "\n")
        if TCPs.flags.ACK == 0:
            text += ("            .... ...0 .... = Push: Not set" + "\n")
        else:
            text += ("            .... ...1 .... = Push: Set" + "\n")
        if TCPs.flags.PSH == 0:
            text += ("            .... .... 0... = Acknowledgment: Not set" + "\n")
        else:
            text += ("            .... .... 1... = Acknowledgment: Set" + "\n")
        if TCPs.flags.RST == 0:
            text += ("            .... .... .0.. = Push: Not set" + "\n")
        else:
            text += ("            .... .... .1.. = Push: Set" + "\n")

        text += ("     Window size value: " + str(TCPs.window) + "\n")
        text += ("     Checksum: 0x" + hex(TCPs.chksum) + " [correct]\n")

        # 计算校验和
        packet = TCPs
        checksum_scapy = TCPs.chksum
        text += ("     Header checksum: " + hex(checksum_scapy) + " [correct]\n")

        # 计算TCP校验和
        packet.chksum = 0
        packet_raw = raw(packet)
        checksum_TCP = in4_chksum(socket.IPPROTO_TCP, IPs , packet_raw)

        if checksum_scapy == checksum_TCP:
            text += ("""     [Header checksum status: Good]-++++++++""" + "\n")
        else:
            text += ("""     [Header checksum status: Bad]""" + "\n")
        text += ("     [Calculated checksum: " + hex(checksum_TCP) + "]\n")

        text += ("     Urgent pointer: " + str(TCPs.urgptr) + "\n")
        text += ("     Options: " + str(TCPs.options) + "\n")

        return text

    def choosedIPPDUAnalysis(self):
        # 请在此处完成IP协议的分析器(分析数据包功能)，并添加详细代码注释
        choosePDUNum = self.listbox.curselection()[0]
        choosedPacket = self.sniffDataList[choosePDUNum]

        # 实现对文本框内的文字进行删除，然后重新打印IP信息
        self.PDUAnalysisText.delete("1.0", END)

        # 打印IP信息-------------------------------------------------------------------
        IPtext = ""
        IPtext += self.addEther(choosedPacket['Ethernet'])
        IPtext += self.addIP(choosedPacket['IP'])

        self.PDUAnalysisText.insert(END, IPtext)

        # 打印原始报文---------------------------------------------------------------------
        self.PDUCodeText.delete("1.0", END)
        # 创建一个StringIO对象，用于捕获hexdump的输出
        output = io.StringIO()
        sys.stdout = output  # 将stdout重定向到StringIO对象

        # 将原始报文输入到控制台
        hexdump(choosedPacket)

        # 从StringIO对象中获取hexdump的输出字符串
        IPBaowen = output.getvalue()

        # 恢复stdout的原始设置
        sys.stdout = sys.__stdout__

        self.PDUCodeText.insert(END,IPBaowen)

    def choosedARPPDUAnalysis(self):
        # 请在此处完成ARP协议的分析器(分析数据包功能)，并添加详细代码注释
        choosePDUNum = self.listbox.curselection()[0]
        choosedPacket = self.sniffDataList[choosePDUNum]

        # 实现对文本框内的文字进行删除，然后重新打印IP信息
        self.PDUAnalysisText.delete("1.0", END)

        # 打印ARP信息---------------------------------------------------------------------
        ARPtext = ("捕获时间：" + str(choosedPacket.time) + "\n")
        if 'Ether' in choosedPacket:
            ARPtext += self.addEther(choosedPacket['Ethernet'])
        ARPtext += self.addARP(choosedPacket['ARP'])

        self.PDUAnalysisText.insert(END, ARPtext)

        # 打印原始报文---------------------------------------------------------------------
        self.PDUCodeText.delete("1.0", END)
        # 创建一个StringIO对象，用于捕获hexdump的输出
        output = io.StringIO()
        sys.stdout = output  # 将stdout重定向到StringIO对象

        # 将原始报文输入到控制台
        hexdump(choosedPacket)

        # 从StringIO对象中获取hexdump的输出字符串
        ARPBaowen = output.getvalue()

        # 恢复stdout的原始设置
        sys.stdout = sys.__stdout__

        self.PDUCodeText.insert(END, ARPBaowen)

    def choosedTCPPDUAnalysis(self):
        # 请在此处完成TCP协议的分析器(分析数据包功能)，并添加详细代码注释
        choosePDUNum = self.listbox.curselection()[0]
        choosedPacket = self.sniffDataList[choosePDUNum]

        # 实现对文本框内的文字进行删除，然后重新打印IP信息
        self.PDUAnalysisText.delete("1.0", END)

        # 打印TCP信息--------------------------------------------------------------------
        TCPtext = ""
        if 'Ether' in choosedPacket:
            TCPtext += self.addEther(choosedPacket['Ethernet'])
        if 'IP' in choosedPacket:
            TCPtext += self.addIP(choosedPacket['IP'])
        TCPtext += self.addTCP(choosedPacket['TCP'],choosedPacket['IP'])

        self.PDUAnalysisText.insert(END, TCPtext)

        # 打印原始报文---------------------------------------------------------------------
        self.PDUCodeText.delete("1.0", END)
        # 创建一个StringIO对象，用于捕获hexdump的输出
        output = io.StringIO()
        sys.stdout = output  # 将stdout重定向到StringIO对象

        # 将原始报文输入到控制台
        hexdump(choosedPacket)

        # 从StringIO对象中获取hexdump的输出字符串
        PDUBaowen = output.getvalue()

        # 恢复stdout的原始设置
        sys.stdout = sys.__stdout__

        self.PDUCodeText.insert(END, PDUBaowen)


    def choosedUDPPDUAnalysis(self):
        # 请在此处完成UDP协议的分析器(分析数据包功能)，并添加详细代码注释
        choosePDUNum = self.listbox.curselection()[0]
        choosedPacket = self.sniffDataList[choosePDUNum]

        # 实现对文本框内的文字进行删除，然后重新打印IP信息
        self.PDUAnalysisText.delete("1.0", END)

        # 打印UDP信息
        UDPtext = ""

        if 'Ether' in choosedPacket:
            UDPtext += self.addEther(choosedPacket['Ethernet'])

        if 'IP' in choosedPacket:
            UDPtext += self.addIP(choosedPacket['IP'])

        UDPtext += ("User Daragram Protocol, Src Port: " + str(choosedPacket['UDP'].sport) + ", Dst Port: " + str(choosedPacket['UDP'].dport) + "\n")
        UDPtext += ("     Source Port: " + str(choosedPacket['UDP'].sport) + "\n")
        UDPtext += ("     Destination Port: " + str(choosedPacket['UDP'].dport) + "\n")
        UDPtext += ("     Length: " + str(choosedPacket['UDP'].len) + "\n")
        UDPtext += ("     Checksum: 0x" + hex(choosedPacket['UDP'].chksum) + " [correct]\n")

        # 计算校验和
        packet = choosedPacket['UDP']
        chksum_scapy = choosedPacket['UDP'].chksum
        UDPtext += ("     Header checksum: " + hex(chksum_scapy) + " [correct]\n")

        packet.chksum = 0
        packet_raw = raw(packet)
        checksum_UDP = in4_chksum(socket.IPPROTO_UDP, choosedPacket['IP'], packet_raw)

        if chksum_scapy == checksum_UDP:
            UDPtext += ("""     [Header checksum status: Good]-++++++++""" + "\n")
        else:
            UDPtext += ("""     [Header checksum status: Bad]""" + "\n")
        UDPtext += ("     [Calculated checksum: " + hex(checksum_UDP) + "]\n")

        self.PDUAnalysisText.insert(END, UDPtext)

        # 打印原始报文---------------------------------------------------------------------
        self.PDUCodeText.delete("1.0", END)
        # 创建一个StringIO对象，用于捕获hexdump的输出
        output = io.StringIO()
        sys.stdout = output  # 将stdout重定向到StringIO对象

        # 将原始报文输入到控制台
        hexdump(choosedPacket)

        # 从StringIO对象中获取hexdump的输出字符串
        UDPBaowen = output.getvalue()

        # 恢复stdout的原始设置
        sys.stdout = sys.__stdout__

        self.PDUCodeText.insert(END, UDPBaowen)

app = Application()
app.mainloop()
