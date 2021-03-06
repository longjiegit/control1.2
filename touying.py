from PyQt5.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QTableWidget,QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QBrush,QColor
import json,socket,time,struct,threading,commonData
from log import Logger
from TyService import TouyingService as tys
import hashlib

class Touying(QWidget):
    updata_startus = pyqtSignal(int, int)
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()
        self.updata_startus.connect(self.updateStatus)
        thr = threading.Thread(target=self.checkThread, args=())
        thr.setDaemon(True)
        thr.start()
    def initData(self):

        self.t = commonData.TERM_DICT['touying']


    def initUI(self):
        checkAll = QPushButton('全选')
        checkAll.clicked.connect(self.allChecked)

        checkCancel = QPushButton('全取消')
        checkCancel.clicked.connect(self.allCanceled)
        startup = QPushButton('开机')
        startup.clicked.connect(self.wake)

        shutdown = QPushButton('关机')
        shutdown.clicked.connect(self.wake)
        hbox = QHBoxLayout()
        hbox.addWidget(checkAll, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addWidget(checkCancel, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addWidget(startup, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addWidget(shutdown, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addStretch(100)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.table = QTableWidget(len(self.t), 5)
        self.table.setHorizontalHeaderLabels(['', '标签', 'IP', '端口','状态'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.resizeRowsToContents()
        self.table.setColumnWidth(0, 30)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for row in range(len(self.t)):
            for column in range(4):
                rownum = QTableWidgetItem()
                rownum.setCheckState(Qt.Unchecked)
                r = list(self.t[row].values())
                # 设置每个位置的文本值
                if column == 0:
                    self.table.setItem(row, 0, rownum)
                else:
                    item = QTableWidgetItem(r[column - 1].strip())
                    self.table.setItem(row, column, item)

        vbox.addWidget(self.table)
        self.setLayout(vbox)
    def allChecked(self):
        for i in range(self.table.rowCount()):
            if(self.table.item(i, 0).checkState()):
                pass
            else:
                self.table.item(i, 0).setCheckState(Qt.Checked)
    def allCanceled(self):
        for i in range(self.table.rowCount()):
            if(self.table.item(i, 0).checkState()):
                self.table.item(i, 0).setCheckState(Qt.Unchecked)
    def wake(self):
        sender = self.sender()
        if sender.text()=='开机':
            for i in range(self.table.rowCount()):
                if (self.table.item(i, 0).checkState()):
                    ip=self.table.item(i,2).text()
                    port = self.table.item(i, 3).text()
                    Logger.getLog().logger.info("远程开启投影机"+ip)
                    # t1 = threading.Thread(target=tys.comm, args=(ip,port,bytes.fromhex('02 50 4F 4E 03'),))
                    t1 = threading.Thread(target=tys.Pjlink, args=(ip, b'%1POWR 1\r',))
                    t1.start()
        else:
            for i in range(self.table.rowCount()):
                if (self.table.item(i, 0).checkState()):
                    ip = self.table.item(i, 2).text()
                    port=self.table.item(i,3).text()
                    Logger.getLog().logger.info('远程关闭投影机'+ip)
                    # t1 = threading.Thread(target=tys.comm, args=(ip,port,bytes.fromhex('02 50 4F 46 03'),))
                    t1=threading.Thread(target=tys.Pjlink,args=(ip,b'%1POWR 0\r',))
                    t1.start()
    def Panasonic(self,ip,port,command):
        try:
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,1024))
            result=s.recv(1024).decode('UTF-8')
            l=list(result)
            x='admin'
            y='admin'
            z = l[12] + l[13] + l[14] + l[15] + l[16] + l[17] + l[18] + l[19]
            s1 = ':'.join((x, y, z))
            m = hashlib.md5(s1.encode())
            cmd = m.hexdigest() + command
            s.send(cmd.encode('utf-8'))
            re = s.recv(1024)
            Logger.getLog().logger.info(re)
        except Exception as e:
            Logger.getLog().logger.error(e)
    def Pjlink(self,ip,port,command):
        try:
            print(ip)
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,port))
            #s.connect((ip,int(port)))
            result=s.recv(1024).decode('UTF-8')
            s.send(command)
            re=s.recv(1024)
            Logger.getLog().logger.info(re)
        except Exception as e:
            Logger.getLog().logger.error(e)
    def comm(self,ip,port,command):
        try:
            s=socket.socket()
            s.settimeout(3)
            s.connect((ip,4196))
            s.send(command)
            re=s.recv(1024)
            Logger.getLog().logger.info(re)
        except Exception as e:
            Logger.getLog().logger.error(e)

    def checkThread(self):
        while True:
            for i in range(len(self.t)):
                ip = self.t[i]['IP']
                check1 = threading.Thread(target=self.checkstatusPJLink, args=(ip, i))
                check1.start()
            time.sleep(30)

    def checkstatusPJLink(self, ip, index):
        try:
            checksocket = socket.socket()
            checksocket.settimeout(2)
            checksocket.connect((ip, 4352))
            result = checksocket.recv(1024).decode('UTF-8')
            l = list(result)
            checksocket.send(b'%1POWR ?\r')
            re = checksocket.recv(1024)
            intstatus = str(re,'utf-8')
            print(intstatus)
            if intstatus == '%1POWR=0':
                self.updata_startus.emit(0, index)
            elif intstatus == '%1POWR=1':
                self.updata_startus.emit(1, index)
            elif intstatus == '%1POWR=2':
                self.updata_startus.emit(2, index)
            elif intstatus == '%1POWR=3':
                self.updata_startus.emit(3, index)
            elif intstatus == '%1POWR=ERR3':
                self.updata_startus.emit(4, index)
            elif intstatus == '%1POWR=ERR4':
                self.updata_startus.emit(5, index)
            checksocket.close()
        except Exception as e:
            self.updata_startus.emit(6, index)
            print("fail")

    def updateStatus(self, stat, index):
        if stat == 0:
            item = QTableWidgetItem("开机")
            item.setForeground(QBrush(QColor(0, 255, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 1:
            item = QTableWidgetItem("关机")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 2:
            item = QTableWidgetItem("冷却中")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 3:
            item = QTableWidgetItem("预热中")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 4:
            item = QTableWidgetItem("不可用")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 5:
            item = QTableWidgetItem("机器故障")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 6:
            item = QTableWidgetItem("离线")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)