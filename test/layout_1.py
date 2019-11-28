from PyQt5.QtWidgets import QWidget,QMainWindow,QPushButton,QHBoxLayout,QVBoxLayout,QApplication,QMenuBar,QStatusBar
import sys
from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btnOK=QPushButton('确定')
        btnCancle=QPushButton('取消')

        hbox=QHBoxLayout()

        hbox.addWidget(QPushButton('123'),0,Qt.AlignLeft|Qt.AlignTop)
        hbox.addWidget(btnOK,0,Qt.AlignLeft|Qt.AlignTop)
        hbox.addWidget(btnCancle,0,Qt.AlignLeft|Qt.AlignTop)
        hbox.addStretch(1)


        # vbox=QVBoxLayout()
        # vbox.addLayout(hbox)


        self.setLayout(hbox)
        self.setGeometry(300,300,800,600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())