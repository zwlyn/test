from PyQt5.Widget import *
from PyQt5.Core import *

class Mcalc(QFrame):
    def __init__(self):
        super().__init__()
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        pass
    
    def initUI(self):
        layout = QHBoxLayout()
        btn = QPushButton()
        layout.addWidget(btn)

        self.setLayout(layout)
        self.show()

    def initConnect(self):
        pass



if __name__ == '__main__':
    