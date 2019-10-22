import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Mcalc(QFrame):
    digitNum = 10
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        pass
    
    def initUI(self):
        self.layout = QHBoxLayout()

        self.createDigitBtn()
        self.setLayout(self.layout)

    def initConnect(self):
        pass

    def createDigitBtn(self):
        box = QWidget()
        numLayout = QGridLayout()
        for num in range(Mcalc.digitNum):
            btn = QPushButton('%d' % num)
            x = 4 - num / 3
            y = num % 3 
            if y == 0:
                y = 3
            if num == 0:
                y = 1
            numLayout.addWidget(btn, x, y)
        box.setLayout(numLayout)
        self.layout.addWidget(box)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Mcalc()
    ui.show()
    sys.exit(app.exec_())