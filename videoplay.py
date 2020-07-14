from PyQt5.QtWidgets import QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QLabel,QTableWidget,QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt
import commonData
from commonservice import VideoService,JDService
import time

class VideoPlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        mainBox=QVBoxLayout()
        self.table = QTableWidget(len(commonData.VIDEO_LIST), 4)
        self.table.setHorizontalHeaderLabels(['名称','操作', 'IP', '端口'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.resizeRowsToContents()

        for row in range(len(commonData.VIDEO_LIST)):
            item = QTableWidgetItem(commonData.VIDEO_LIST[row][3])
            self.table.setItem(row, 0, item)
            item0 = QTableWidgetItem(commonData.VIDEO_LIST[row][1])
            self.table.setItem(row, 2, item0)
            item1 = QTableWidgetItem(commonData.VIDEO_LIST[row][2])
            self.table.setItem(row, 3, item1)
            self.table.setCellWidget(row,1,self.buttonForRow(row))
            self.table.setRowHeight(row,40)
        mainBox.addWidget(self.table,Qt.AlignTop)
        self.setLayout(mainBox)
    def buttonForRow(self,id):
        widget = QWidget()
        hLbox = QHBoxLayout()
        playBtn = QPushButton('播放')
        playBtn.clicked.connect(lambda :self.play(id))
        stopBtn = QPushButton('停止')
        stopBtn.clicked.connect(lambda :self.stop(id))
        hLbox.addWidget(playBtn)
        hLbox.addWidget(stopBtn)
        hLbox.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLbox)
        return widget
    def play(self,row):
        video=commonData.VIDEO_LIST[row]
        """灯光关"""
        try:
            index=video[4]
            lines=video[5]
            lineList=lines.split("#")
            self.device = commonData.JD_DICT['devices'][int(index)-1]
            for lineNum in lineList:
                line=int(lineNum)
                IP = self.device['device'][line - 1]['ip']
                port = self.device['device'][line - 1]['port']
                dest = self.device['device'][line - 1]['road']
                addr =self.device['device'][line - 1]['addr']
                cmod = JDService.getSingleCommand(hex(addr), hex(dest - 1), '0000')
                JDService.sendCommand(IP,port,cmod)
                time.sleep(0.3)
        except Exception as e:
            print(e)
        VideoService.sendVideoCommand(video[1],'play')
        # VideoService.sendVideoCommand(video[1],'play')
    def stop(self,row):
        video = commonData.VIDEO_LIST[row]
        """灯光开"""
        try:
            index = video[4]
            lines = video[5]
            lineList = lines.split("#")
            self.device = commonData.JD_DICT['devices'][int(index) - 1]
            for lineNum in lineList:
                line = int(lineNum)
                IP = self.device['device'][line - 1]['ip']
                port = self.device['device'][line - 1]['port']
                dest = self.device['device'][line - 1]['road']
                addr = self.device['device'][line - 1]['addr']
                cmod = JDService.getSingleCommand(hex(addr), hex(dest - 1), 'FF00')
                JDService.sendCommand(IP, port, cmod)
                time.sleep(0.3)
        except Exception as e:
            print(e)
        VideoService.sendVideoCommand(video[1], 'stop')