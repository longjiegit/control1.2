import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

class MainWindow(QWidget):
    closeSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MainWindow Demo")
        self.resize(800, 600)

        button = QPushButton("close", self)
        # 连接内置信号与自定义槽
        button.clicked.connect(self.onClicked)
        # 连接自定义信号closeSignal与内置槽函数close
        self.closeSignal.connect(self.onClose)

    # 自定义槽函数
    def onClicked(self):
        # 发送自定义信号
        self.closeSignal.emit('我是谁')

    # 自定义槽函数
    def onClose(self,n):
        print(n)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())