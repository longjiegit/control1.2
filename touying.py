from PyQt5.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QTableWidget,QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt
import json,socket,time,struct,threading,commonData
from log import Logger
import hashlib

class Touying(QWidget):
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()

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

        self.table = QTableWidget(len(self.t), 4)
        self.table.setHorizontalHeaderLabels(['', '标签', 'IP', '端口'])
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
                    t1 = threading.Thread(target=self.comm, args=(ip,port,bytes.fromhex('02 50 4F 4E 03'),))
                    t1.start()
        else:
            for i in range(self.table.rowCount()):
                if (self.table.item(i, 0).checkState()):
                    ip = self.table.item(i, 2).text()
                    port=self.table.item(i,3).text()
                    Logger.getLog().logger.info('远程关闭投影机'+ip)
                    t1 = threading.Thread(target=self.comm, args=(ip,port,bytes.fromhex('02 50 4F 46 03'),))
                    t1.start()

    def Pjlink(self,ip,port,command):
        try:
            print(ip)
            s=socket.socket()
            s.settimeout(3)
            s.connect(('192.168.1.158',4352))
            #s.connect((ip,int(port)))
            result=s.recv(1024).decode('UTF-8')
            l = list(result)
            print(l)
            x = 'dispadmin'
            y = 'admin'
            z = l[9]+l[10]+l[11]+l[12]+l[13]+l[14]+l[15]+l[16]
            s1 = ':'.join((x, y, z));
            print(s1)
            m = hashlib.sha3_256(s1.encode())
            print(m)
            cmd=m.hexdigest()+'%1POWR 0\r'
            print(cmd)
            s.send(cmd.encode())
            print('end')
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