from PyQt5.QtCore import *


class SignalManager(QObject):

    buttonClicked = pyqtSignal(str) # view发送到controller
    nameChanged = pyqtSignal(dict,dict)  # conntroller 发送到view

    def __init__(self):
        super(SignalManager, self).__init__()

signalManager = SignalManager()