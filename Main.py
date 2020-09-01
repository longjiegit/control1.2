import sys,os
os.environ['path'] = os.getenv('path') + ";" + os.path.abspath('./lib')
print(os.getenv('path'))
from PyQt5.QtWidgets import QWidget,QApplication,QVBoxLayout,QLabel,QFrame,QMessageBox
import comput,touying,jd,videoplay,threading,Impl,UdpImpl,commonData
from log import Logger
import time,util,commonData

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        Logger.getLog().logger.info('程序启动')
        self.initUI()
        self.setMinimumWidth(1024)
        self.setMinimumHeight(700)

    def initUI(self):
        self.f=QFrame(self)
        # self.tableview = QTabWidget(self)
        vbox=QVBoxLayout()


        self.tb1=comput.Comput(commonData.SENDSIG)
        self.tb1.resize(500,300)


        self.tb2=touying.Touying()
        self.tb2.resize(500, 300)

        self.tb3=jd.Jd(commonData.SENDSIG,commonData.RECSIG)
        self.tb3.resize(500,300)

        self.tb4=videoplay.VideoPlay()
        self.tb4.resize(500,300)

        lab1=QLabel('强电控制')
        vbox.addWidget(lab1)
        vbox.addWidget(self.tb3)
        lab2 = QLabel('PC控制')
        vbox.addWidget(lab2)
        vbox.addWidget(self.tb1)
        lab3 = QLabel('投影控制')
        vbox.addWidget(lab3)
        vbox.addWidget(self.tb2)
        lab4 = QLabel('播放控制')
        vbox.addWidget(lab4)
        vbox.addWidget(self.tb4)

        self.f.setLayout(vbox)
        self.f.setObjectName("mainwindow")
        self.f.setStyleSheet("#mainwindow{border-image:url(./img/back.jpg)}")
        self.setWindowTitle('中控程序')
        # self.tableview.addTab(self.f,'123')
        self.setGeometry(200,200,1140,800)
        # self.tableview.resize(1140,800)

    def resizeEvent(self, QResizeEvent):
        w=QResizeEvent.size().width()
        h=QResizeEvent.size().height()
        # self.tableview.resize(w,h)
        self.f.resize(w,h)

    def showDerlMessage(self,message):
        messageBox=QMessageBox()
        messageBox.setWindowTitle('警告')
        messageBox.setText(message)
        messageBox.setStandardButtons(QMessageBox.Yes)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        # messageBox.resize(300,300)
        messageBox.move(600,500)

        messageBox.exec_()
        if messageBox.clickedButton() == buttonY:
            sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = MainWindow()
    table.show()
    '''注册码验证'''
    # now_time = time.time()
    # try:
    #     zl = bytes(commonData.REGIST, encoding='utf-8')
    # except Exception as e:
    #     print(e)
    #     table.showDerlMessage('无法获取注册码')
    # try:
    #     zl2 = util.Util.des_descrypt(zl)
    #     list = zl2.split('-')
    #     t1_str = list[1].rstrip('a')
    #     start_time = int(t1_str)
    # except Exception as e:
    #     table.showDerlMessage('无效注册码')
    # print(start_time)
    # print(now_time - start_time)
    # print(int(list[0]))
    # print('aaa')
    # if(int((now_time - start_time) / 3600/24)>int(list[0])):
    #     table.showDerlMessage('注册码过期')
    imp=Impl.TablePad()
    t1= threading.Thread(target=imp.start, args=())
    t1.setDaemon(True)
    t1.start()
    # udpser=UdpImpl.UdpServer()
    # t2=threading.Thread(target=udpser.startServer,args=())
    # t2.setDaemon(True)
    # t2.start()

    sys.exit(app.exec_())