    
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from signalmanager import signalManager

class UI2(QWidget):
    """docstring for UI2"""
    def __init__(self):
        super(UI2,self).__init__()
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        pass

    def initUI(self):
        layout = QFormLayout()

        btn1 = QPushButton('一个骄傲的button')
        btn2 = QPushButton('btn2')
        label = QLabel('测试：')
        self.lineEdit1 = QLineEdit()
        lineEdit2 = QLineEdit()
        lineEdit3 = QLineEdit()
        layout.addRow(btn1)
        layout.addRow(btn2)
        layout.addRow(label, self.lineEdit1)
        layout.addRow(lineEdit2)
        layout.addRow(lineEdit3)

        self.setLayout(layout)


    def  initConnect(self):

        signalManager.nameChanged.connect(self.fun)

    def fun(self, msg1, msg2):
        print(msg1, type(msg1))
        print(msg2, type(msg2))




