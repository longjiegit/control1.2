import sys,os
os.environ['path'] = os.getenv('path') + ";" + os.path.abspath('./lib')
print(os.getenv('path'))
from PyQt5.QtWidgets import QWidget,QTabWidget,QApplication,QVBoxLayout,QLabel,QFrame
import comput,touying,jd,videoplay,threading,Impl,commonData
from log import Logger
from MySignal import SignalClass

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        Logger.getLog().logger.info('程序启动')
        self.sc=SignalClass()
        self.initUI()
        self.setMinimumWidth(1024)
        self.setMinimumHeight(700)

    def initUI(self):
        self.f=QFrame(self)
        # self.tableview = QTabWidget(self)
        vbox=QVBoxLayout()


        self.tb1=comput.Comput(self.sc)
        self.tb1.resize(500,300)


        self.tb2=touying.Touying()
        self.tb2.resize(500, 300)

        self.tb3=jd.Jd(self.sc)
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
        self.f.setStyleSheet("#mainwindow{border-image:url(./img/bg4.jpg)}")
        self.setWindowTitle('中控程序')
        # self.tableview.addTab(self.f,'123')
        self.setGeometry(200,200,1140,800)
        # self.tableview.resize(1140,800)

    def resizeEvent(self, QResizeEvent):
        w=QResizeEvent.size().width()
        h=QResizeEvent.size().height()
        # self.tableview.resize(w,h)
        self.f.resize(w,h)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    table = MainWindow()

    table.show()
    imp=Impl.TablePad()
    t1 = threading.Thread(target=imp.start, args=())
    t1.setDaemon(True)
    t1.start()
    sys.exit(app.exec_())