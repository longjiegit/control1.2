from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QPushButton,QDesktopWidget,QAction,qApp,QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
import  sys

class Frame(QMainWindow):
    def __init__(self):
        super(Frame, self).__init__()
        self.initUI()
        self.initMenu()
    def initMenu(self):
        exitAct=QAction(QIcon('./ico/1.jpg'),'&Exit',self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('exit app')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()
        '''创建菜单条'''
        menubar=self.menuBar()
        fileMenu=menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        '''子菜单'''
        impMenu=QMenu('import',self)
        impAct=QAction('import mail',self)
        '''添加子菜单条目'''
        impMenu.addAction(impAct)
        '''在fileMenu下添加子菜单'''
        fileMenu.addMenu(impMenu)

        viewMene=menubar.addMenu('view')
        viewStatAct=QAction('view status',self,checkable=True)
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toggleMenu)

        viewMene.addAction(viewStatAct)

    def toggleMenu(self, state):
        pass

    def initUI(self):

        self.setToolTip('this is a qwidget')
        btn=QPushButton('Button',self)
        btn.setToolTip('this is a pushbutton')
        btn.resize(btn.sizeHint())
        btn.move(50,50)

        quit=QPushButton('quit',self)
        quit.resize(quit.sizeHint())
        quit.move(150,50)

        quit.clicked.connect(QCoreApplication.instance().quit)
        self.setWindowIcon(QIcon('./ico/1.jpg'))
        self.setWindowTitle('first demo')
        # self.setGeometry(200,200,400,600)
        self.resize(600,400)
        self.center()
        self.show()
    def center(self):
        qr=self.frameGeometry()
        print(qr)
        cp=QDesktopWidget().availableGeometry().center()
        print(cp)
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        print(qr.topLeft())
if __name__=='__main__':
    app=QApplication(['123'])
    frame=Frame()
    sys.exit(app.exec_())