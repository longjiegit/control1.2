from PyQt5.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QTableWidget,QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QBrush,QColor
from log import Logger
import json,socket,time,struct,threading,commonData,commonservice
from commonservice import ComputService as cs


class Comput(QWidget):
    updata_startus = pyqtSignal(int, int)
    def __init__(self,sc):
        super().__init__()
        self.sc=sc
        self.t = commonData.TERM_DICT['comput']
        self.initUI()
        self.updata_startus.connect(self.updateStatus)
        thr = threading.Thread(target=self.checkThread, args=())
        thr.setDaemon(True)
        thr.start()


    def initUI(self):
        checkAll=QPushButton('全选')
        checkAll.clicked.connect(self.allChecked)

        checkCancel=QPushButton('全取消')
        checkCancel.clicked.connect(self.allCanceled)
        startup=QPushButton('开机')
        startup.clicked.connect(self.wake)

        shutdown=QPushButton('关机')
        shutdown.clicked.connect(self.shutdownComput)
        hbox=QHBoxLayout()
        hbox.addWidget(checkAll,1,Qt.AlignLeft|Qt.AlignTop)
        hbox.addWidget(checkCancel, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addWidget(startup, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addWidget(shutdown, 1, Qt.AlignLeft | Qt.AlignTop)
        hbox.addStretch(100)
        vbox=QVBoxLayout()
        vbox.addLayout(hbox)


        self.table=QTableWidget(len(self.t),5)
        self.table.setHorizontalHeaderLabels(['','标签','IP','MAC地址','状态'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.resizeRowsToContents()
        self.table.setColumnWidth(0,30)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        for row in range(len(self.t)):
            for column in range(4):
                rownum= QTableWidgetItem()
                rownum.setCheckState(Qt.Unchecked)
                r=list(self.t[row].values())
                #设置每个位置的文本值
                if column==0:
                    self.table.setItem(row, 0, rownum)
                else:
                    item = QTableWidgetItem(r[column-1].strip())
                    self.table.setItem(row,column,item)
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
        for i in range(self.table.rowCount()):
            if (self.table.item(i, 0).checkState()):

                mac=self.table.item(i,3).text()
                # self.sc.sendText("".join(("开启电脑", mac)))
                t1 = threading.Thread(target=cs.wake_up, args=(mac,))
                t1.start()
    def wake_up(self,mac='DC-4A-3E-78-3E-0A'):
        try:
            MAC = mac
            BROADCAST = "255.255.255.255"
            if len(MAC) != 17:
                raise ValueError("MAC address should be set as form 'XX-XX-XX-XX-XX-XX'")
            mac_address = MAC.replace("-", '')
            data = ''.join(['FFFFFFFFFFFF', mac_address * 20])  # 构造原始数据格式
            send_data = b''

            # 把原始数据转换为16进制字节数组，
            for i in range(0, len(data), 2):
                send_data = b''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])
            Logger.getLog().logger.info(':'.join(('远程唤醒',mac,'网关',BROADCAST)))

        # 通过socket广播出去，为避免失败，间隔广播三次

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # sock.sendto(send_data, (BROADCAST, 7))
            # time.sleep(1)
            sock.sendto(send_data, (BROADCAST, 7))
            # time.sleep(1)
            # sock.sendto(send_data, (BROADCAST, 7))
        except Exception as e:
            Logger.getLog().logger.error(e)
    def shutdownComput(self):
        for i in range(self.table.rowCount()):
            if (self.table.item(i, 0).checkState()):
                ip=self.table.item(i,2).text()
                command='shutdown -s -f -t 00'
                # self.sc.sendText("".join(("关闭电脑",ip)))
                t1 = threading.Thread(target=cs.shutComput, args=(ip,command,))
                t1.start()
    def shutComput(self,ip,command):
        try:
            Logger.getLog().logger.info("远程关闭主机"+ip)
            s=socket.socket()
            s.connect((ip,8000))
            data = '{"type":"cmd","data":"' + command + '"}'
            s.send(bytes(data,encoding='UTF-8'))
            s.close()
        except Exception as e:
            Logger.getLog().logger.error("远程关机失败"+ip)
            Logger.getLog().logger.error(e)

    def checkThread(self):
        while True:
            for i in range(len(self.t)):
                ip = self.t[i]['IP']
                check1 = threading.Thread(target=self.checkstatus, args=(ip, i))
                check1.start()

            time.sleep(30)

    def checkstatus(self, ip, index):
        try:
            checksocket = socket.socket()
            checksocket.settimeout(2)
            intstatus = checksocket.connect_ex((ip, 5800))
            if intstatus == 10061:
                self.updata_startus.emit(1, index)
            elif intstatus == 0:
                self.updata_startus.emit(1, index)
            elif intstatus == 10035:
                self.updata_startus.emit(0, index)
            checksocket.close()
        except Exception as e:
            print("fail")

    def updateStatus(self, stat, index):
        if stat == 0:
            item = QTableWidgetItem("离线")
            item.setForeground(QBrush(QColor(255, 0, 0)))
            self.table.setItem(index, 4, item)
        elif stat == 1:
            item = QTableWidgetItem("在线")
            item.setForeground(QBrush(QColor(0, 255, 0)))
            self.table.setItem(index, 4, item)