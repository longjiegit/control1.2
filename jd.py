from PyQt5.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QTextEdit,QCheckBox,QTimeEdit
from PyQt5.QtCore import Qt,pyqtSignal,QTime
import json,socket,time,struct,threading
from binascii import *
from crcmod import *
from log import Logger
import codecs,commonData
import  datetime
import configparser
from commonservice import ComputService as cs
from MySignal import SignalClass
class Jd(QWidget):
    updata_resTxt=pyqtSignal(str)
    def __init__(self,sc):
        super().__init__()
        self.initData()
        self.initUI()
        self.updata_resTxt.connect(self.updateRecText)
        sc.textSignal.connect(self.updateSendText)
        self.addListen()
    #   启动一个线程定时执行任务
        time_start_shut=threading.Thread(target=self.timeStartShut,args=())
        time_start_shut.setDaemon(True)
        time_start_shut.start()


    def initData(self):
        self.t = commonData.TERM_DICT['touying']
        self.cpt = commonData.TERM_DICT['comput']
        self.cf=configparser.ConfigParser()
        self.cf.read("./config/timeconfig.ini")
        self.devices=commonData.JD_DICT['devices']
        self.size=len(self.devices)

        self.cbox =self.size* ['']
        self.open_btn =self.size* ['']
        self.shut_btn =self.size* ['']

    def timeStartShut(self):
        Logger.getLog().logger.info("计时器启动")
        oldstime=''
        newstime=datetime.datetime.now()
        oldctime=''
        newctime=datetime.datetime.now()
        while True:
            week = []
            if self.monday.checkState():
                week.append(1)
            if self.tuesday.checkState():
                week.append(2)
            if self.wenday.checkState():
                week.append(3)
            if self.thurday.checkState():
                week.append(4)
            if self.friday.checkState():
                week.append(5)
            if self.satday.checkState():
                week.append(6)
            if self.sunday.checkState():
                week.append(7)

            now = datetime.datetime.now()

            weekday=now.isoweekday()
            if(self.tstart.checkState()):
                if weekday in week:
                    if (now.hour==self.stimeEdit.time().hour()) and (now.minute==self.stimeEdit.time().minute()):
                        oldstime=newstime
                        newstime=now
                        if(newstime-oldstime).seconds>60:
                            Logger.getLog().logger.info('定时开机启动')
                            self.onKeyOpen()
            if(self.tclose.checkState()):
                if weekday in week:
                    if (now.hour == self.ctimeEdit.time().hour()) and (now.minute == self.ctimeEdit.time().minute()):
                        oldctime=newctime
                        newctime=now
                        if(newctime-oldctime).seconds>60:
                            Logger.getLog().logger.info('定时关机启动')
                            self.onKeyClose()
            time.sleep(35)
    def initUI(self):

        hbox=QHBoxLayout()
        self.monday=QCheckBox("周一")
        if self.cf.getint('date','monday'):
            self.monday.setChecked(True)
        self.tuesday=QCheckBox('周二')
        if self.cf.getint('date','tuesday'):
            self.tuesday.setChecked(True)
        self.wenday = QCheckBox('周三')
        if self.cf.getint('date', 'wenday'):
            self.wenday.setChecked(True)
        self.thurday = QCheckBox('周四')
        if self.cf.getint('date', 'thurday'):
            self.thurday.setChecked(True)
        self.friday = QCheckBox('周五')
        if self.cf.getint('date', 'friday'):
            self.friday.setChecked(True)
        self.satday = QCheckBox('周六')
        if self.cf.getint('date', 'satday'):
            self.satday.setChecked(True)
        self.sunday = QCheckBox('周日')
        if self.cf.getint('date', 'sunday'):
            self.sunday.setChecked(True)
        self.tstart = QCheckBox('开启')
        if self.cf.getint('date', 'tstart'):
            self.tstart.setChecked(True)
        self.tclose = QCheckBox('关闭')
        if self.cf.getint('date', 'tclose'):
            self.tclose.setChecked(True)
        stimeLable = QLabel('开启时间：')

        self.stimeEdit = QTimeEdit()
        self.stimeEdit.setMinimumWidth(80)
        d=self.cf.get('date','stimeEdit').split(':')
        print(d)
        self.stimeEdit.setTime(QTime(int(d[0]),int(d[1]),0))
        ctimeLable = QLabel('关闭时间：')

        self.ctimeEdit = QTimeEdit()
        d2 = self.cf.get('date', 'ctimeEdit').split(':')
        self.ctimeEdit.setTime(QTime(int(d2[0]), int(d2[1]), 0))
        self.ctimeEdit.setMinimumWidth(80)


        hbox.addWidget(self.monday,1,Qt.AlignLeft|Qt.AlignCenter)
        hbox.addWidget(self.tuesday, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.wenday, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.thurday, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.friday, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.satday, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.sunday, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(stimeLable,1,Qt.AlignLeft|Qt.AlignCenter)
        hbox.addWidget(self.stimeEdit,1,Qt.AlignLeft|Qt.AlignCenter)
        hbox.addWidget(ctimeLable, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.ctimeEdit, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.tstart, 1, Qt.AlignLeft | Qt.AlignCenter)
        hbox.addWidget(self.tclose, 1, Qt.AlignLeft | Qt.AlignCenter)
        self.startAllBtn=QPushButton("一键全开")
        self.startAllBtn.clicked.connect(self.onKeyOpen)
        self.shutDownAllBtn=QPushButton("全关闭")
        self.shutDownAllBtn.clicked.connect(self.onKeyClose)
        hbox.addWidget(self.startAllBtn,1,Qt.AlignLeft|Qt.AlignTop)
        hbox.addWidget(self.shutDownAllBtn,1,Qt.AlignLeft|Qt.AlignTop)
        hbox.addStretch(50)
        vbox=QVBoxLayout()
        vbox.addLayout(hbox)
        vbox1=QVBoxLayout()
        vbox1.addStretch(10)
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()

        for d in range(len(self.devices)):
            hbox1=QHBoxLayout()
            namelabel=QLabel(self.devices[d]['name'])
            namelabel.setMinimumWidth(80)
            hbox1.addWidget(namelabel,0,Qt.AlignLeft|Qt.AlignTop)
            self.cbox[d]=QComboBox()
            self.cbox[d].setMinimumWidth(100)

            dev=self.devices[d]['device']
            self.cbox[d].addItem("--全部--")
            for t in dev:

                self.cbox[d].addItem(t['label'],t['road'])
            hbox1.addWidget(self.cbox[d],1,Qt.AlignLeft|Qt.AlignTop)
            self.open_btn[d]=QPushButton("打开")
            hbox1.addWidget(self.open_btn[d], 1, Qt.AlignLeft | Qt.AlignTop)
            self.shut_btn[d]=QPushButton("关闭")
            hbox1.addWidget(self.shut_btn[d], 1, Qt.AlignLeft | Qt.AlignTop)
            hbox1.addStretch(100)
            vbox1.addLayout(hbox1)
        vbox1.addStretch(200)
        contentbox=QHBoxLayout()
        contentbox.addLayout(vbox1)
        recordLable=QLabel('发送记录')
        self.sendText=QTextEdit()
        vbox2.addWidget(recordLable)
        vbox2.addWidget(self.sendText)
        contentbox.addLayout(vbox2)
        resultLable=QLabel('返回结果')
        self.resultText=QTextEdit()
        vbox3.addWidget(resultLable)
        vbox3.addWidget(self.resultText)
        contentbox.addLayout(vbox3)

        vbox.addLayout(contentbox)

        self.setLayout(vbox)

        for i in range(self.size):
            self.open_btn[i].clicked.connect(self.onOpen)
            self.shut_btn[i].clicked.connect(self.onShut)

    def updateRecText(self,content):
        self.resultText.append(content)
    def updateSendText(self,content):
        self.sendText.append(content)
    def onKeyOpen(self):

        t=threading.Thread(target=self.keyOpen,args=())
        t.start()
    def keyOpen(self):
        '''先开继电器，然后开投影，然后开电脑'''
        self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'), '继电器全开')))
        for d in range(len(self.devices)):
            dev = self.devices[d]['device']
            for t in dev:
                ip=t['ip']
                port=t['port']
                addr = t['addr']
                road = t['road'] - 1
                print(hex(road))
                cmod = self.getSingleCommand(hex(addr), hex(road), 'FF00')
                self.sendCommand(ip,port,cmod,'继电器全开')
                time.sleep(0.3)
        self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'), '投影全开')))

        for ty in self.t:
            Logger.getLog().logger.info('开启投影机'+ty['IP'])
            self.comm(ty['IP'],4196,bytes.fromhex('02 50 4F 4E 03'))
        time.sleep(30)
        '''电脑全开'''
        self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'), '电脑全开')))
        for c in self.cpt:
            cs.wake_upfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
    def Pjlink(self, ip, command):
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip, 4352))
            result = s.recv(1024).decode('UTF-8')
            l = list(result)
            if l[7] == '0':
                s.send(command)
                re = s.recv(1024)
                Logger.getLog().logger.info(re)
                act_name ="投影"+ip+"响应"
                res = ":".join((time.strftime('%Y-%m-%d %H:%M:%S'), act_name, str(re,'utf-8')))
                self.updata_resTxt.emit(res)
        except Exception as e:
            Logger.getLog().logger.error(e)
    def comm(ip,port,command):
        try:
            Logger.getLog().logger.info('发送指令到投影' + str(command,'utf-8'))
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip, port))
            s.send(command)
            re=s.recv(1024)
            Logger.getLog().logger.info('投影返回结果')
            Logger.getLog().logger.info(str(re,'utf-8'))
        except Exception as e:
            Logger.getLog().logger.error(e)

    def onKeyClose(self):
        t = threading.Thread(target=self.keyClose, args=())
        t.start()
    def keyClose(self):
        '''一键全关只能关闭电脑，然后关闭投影，间隔4分钟后，最后继电器'''
        self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'), '电脑全关')))

        for c in self.cpt:
            cs.shutComputfromJd(c['ip2'],c['port2'],c['addr'],c['road'])
            time.sleep(0.1)
        self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'), '投影全关')))
        for ty in self.t:
            Logger.getLog().logger.info('关闭投影机'+ty['IP'])
            self.comm(ty['IP'],4196,bytes.fromhex('02 50 4F 46 03'))
        Logger.getLog().logger.info('等待50秒')
        time.sleep(50)
        self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'), '继电器全关')))
        for d in range(len(self.devices)):
            dev = self.devices[d]['device']
            for t in dev:
                ip = t['ip']
                port = t['port']
                addr = t['addr']
                road = t['road'] - 1
                if (addr==2) and (road==2):
                    print("no close")
                elif (addr == 1) and (road == 4):
                    print("no close")
                else:
                    cmod = self.getSingleCommand(hex(addr), hex(road), '0000')
                    self.sendCommand(ip, port, cmod, '继电器全关')
                    time.sleep(0.3)

    def onOpen(self):
        dex=self.open_btn.index(self.sender())

        if self.cbox[dex].currentText()=='--全部--':
            '''一个一个的开启'''
            act_name=self.devices[dex]['name']+"全开"
            t1=threading.Thread(target=self.LableOpen,args=(self.devices[dex]['device'],act_name))
            t1.start()
            self.sendText.append(":".join((time.strftime('%Y-%m-%d %H:%M:%S'),act_name)))
            Logger.getLog().logger.info(act_name)
        else:
            index = self.cbox[dex].currentIndex()

            IP = self.devices[dex]['device'][index - 1]['ip']
            port = self.devices[dex]['device'][index - 1]['port']
            dest = self.cbox[dex].currentData()
            addr = self.devices[dex]['device'][index - 1]['addr']

            cmod=self.getSingleCommand(hex(addr), hex(dest-1), 'FF00')
            print(cmod)
            act_name=self.devices[dex]['device'][index - 1]['label']+"开启"
            t = threading.Thread(target=self.sendCommand, args=(IP,port,cmod,act_name,))
            t.start()
            txt=":".join((time.strftime('%Y-%m-%d %H:%M:%S'),act_name))
            Logger.getLog().logger.info(act_name)
            self.sendText.append(txt)
    def LableOpen(self,list,act_name):
        for n in list:
            addr=n['addr']
            dest=hex(n['road']-1)
            cmod = self.getSingleCommand(hex(addr), dest, 'FF00')
            t = threading.Thread(target=self.sendCommand, args=(n['ip'],n['port'],cmod,act_name,))
            t.start()
            time.sleep(1)
    def onShut(self):
        dex = self.shut_btn.index(self.sender())

        if self.cbox[dex].currentText()=='--全部--':
            act_name = self.devices[dex]['name'] + "全关"
            t = threading.Thread(target=self.labelShut, args=(self.devices[dex]['device'],act_name,))
            t.start()
            self.sendText.append(':'.join((time.strftime('%Y-%m-%d %H:%M:%S'),act_name)))
            Logger.getLog().logger.info(act_name)
        else:
            index = self.cbox[dex].currentIndex()
            print(self.cbox[dex].currentIndex())
            IP = self.devices[dex]['device'][index - 1]['ip']
            port = self.devices[dex]['device'][index - 1]['port']
            dest = self.cbox[dex].currentData()
            addr = self.devices[dex]['device'][index - 1]['addr']
            cmod=self.getSingleCommand(hex(addr),hex(dest-1),'0000')
            act_name = self.devices[dex]['device'][index - 1]['label'] + "关闭"
            t=threading.Thread(target=self.sendCommand,args=(IP,port,cmod,act_name,))
            t.start()
            txt = ":".join((time.strftime('%Y-%m-%d %H:%M:%S'), act_name))
            self.sendText.append(txt)
            Logger.getLog().logger.info(act_name)
    def labelShut(self,list,act_name):
        for n in list:
            addr=n['addr']
            dest=hex(n['road']-1)
            cmod = self.getSingleCommand(hex(addr), dest, '0000')
            t = threading.Thread(target=self.sendCommand, args=(n['ip'],n['port'],cmod,act_name,))
            t.start()
            time.sleep(0.5)

    def getMutilCommand(self,addr,num,onOFF='0100'):
        s1='0F000000'
        return "".join((self.hexToString(addr),s1,self.hexToString(num),onOFF))
    def getSingleCommand(self,addr,dest,onOFF):
        s1='0500'
        return "".join((self.hexToString(addr),s1,self.hexToString(dest),onOFF))

    def hexToString(self,str):
        str_list = list(str)
        if len(str_list)==3:
            str_list.insert(2, '0')
        return "".join(str_list[2:])
    def sendCommand(self,ip,port,comd,act_name):
        try:
            data =self.crc16Add(comd)
            a_bytes = bytes.fromhex(data)
            Logger.getLog().logger.info(':'.join((ip,str(port))))
            Logger.getLog().logger.info(comd)
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip,port))
            s.send(a_bytes)
            '''还需要读取返回值'''
            re=s.recv(1024)
            Logger.getLog().logger.info(re)
            aa = ''.join(['%02x' % b for b in re])
            act_name=act_name+"响应"
            res=":".join((time.strftime('%Y-%m-%d %H:%M:%S'),act_name,aa))
            self.updata_resTxt.emit(res)
        except Exception as e:
            Logger.getLog().logger.error(e)

    def crc16Add(self,read):
        # crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        crc16 = crcmod.predefined.mkCrcFun("modbus")

        data = read.replace(" ", "")
        readcrcout = hex(crc16(unhexlify(data))).upper()
        str_list = list(readcrcout)
        if len(str_list) == 5:
            str_list.insert(2, '0')  # 位数不足补0
        elif len(str_list) == 4:
            str_list.insert(2, '0')
            str_list.insert(2, '0')
        crc_data = "".join(str_list)
        read = read.strip() + ' ' + crc_data[4:] + ' ' + crc_data[2:4]
        return read
    def changCheck(self,btn,name):
        print(name)
        if btn.checkState():
            self.cf.set('date',name,'1')
        else:
            self.cf.set('date',name,'0')
        with open('./config/timeconfig.ini','w+') as f:
            self.cf.write(f)
    def changDateTime(self,btn,name):
        h=str(btn.time().hour())
        m=str(btn.time().minute())
        self.cf.set('date',name,':'.join((h,m)))
        with open('./config/timeconfig.ini', 'w+') as f:
            self.cf.write(f)
    def addListen(self):
        self.monday.stateChanged.connect(lambda :self.changCheck(self.monday,'monday'))
        self.tuesday.stateChanged.connect(lambda: self.changCheck(self.tuesday, 'tuesday'))
        self.wenday.stateChanged.connect(lambda: self.changCheck(self.wenday, 'wenday'))
        self.thurday.stateChanged.connect(lambda: self.changCheck(self.thurday, 'thurday'))
        self.friday.stateChanged.connect(lambda: self.changCheck(self.friday, 'friday'))
        self.satday.stateChanged.connect(lambda: self.changCheck(self.satday, 'satday'))
        self.sunday.stateChanged.connect(lambda: self.changCheck(self.sunday, 'sunday'))
        self.tstart.stateChanged.connect(lambda: self.changCheck(self.tstart, 'tstart'))
        self.tclose.stateChanged.connect(lambda: self.changCheck(self.tclose, 'tclose'))
        self.stimeEdit.dateTimeChanged.connect(lambda :self.changDateTime(self.stimeEdit,'stimeEdit'))
        self.ctimeEdit.dateTimeChanged.connect(lambda :self.changDateTime(self.ctimeEdit,'ctimeEdit'))