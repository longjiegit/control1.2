from PyQt5.QtCore import QObject,pyqtSignal

class SignalClass(QObject):
    textSignal=pyqtSignal(str)

    def sendText(self,text):
       self.textSignal.emit(text)

class RecvSignalClass(QObject):
    textSignal=pyqtSignal(str)

    def sendText(self,text):
        self.textSignal.emit(text)