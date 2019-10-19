
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UI2 import UI2
from signalmanager import signalManager

class UI1(QWidget):
    """docstring for Ui1"""
    def __init__(self,parent=None):
        super(UI1, self).__init__(parent)
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        pass

    def initUI(self):
        self.box = UI2()

        layout = QHBoxLayout()
        btn1 = QPushButton('谦虚的Button')

        # widget = QWidget()
        # btn2 = UI2(widget)
        # self.setCentralWidget(btn2)

        # # self.setCentralWidget(btn2)

        layout.addWidget(self.box)
        layout.addWidget(btn1)

        # layout.addStretch(1)
        layout2 = QHBoxLayout()
        btn3 = QPushButton('btn3')
        layout2.addWidget(btn3)
        layout.addLayout(layout2)
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('UI1')
        self.setLayout(layout)

    def initConnect(self):
        self.box.lineEdit1.textEdited.connect(self.fun)

    def fun(self):
        print('textEdited!!!')
        name1 = {
        "who":"QLineEdit1",
        "what":"nameChanged1"
        }
        name2 = {
        "who":"QLineEdit1",
        "what":"nameChanged2"
        }
        signalManager.nameChanged.emit(name1, name2)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui1 = UI1()
    ui1.show()
    sys.exit(app.exec_())
