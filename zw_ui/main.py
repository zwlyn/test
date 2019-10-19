import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from log import logger
from textEditBox import TextEditBox 

class MainWindow(QFrame):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()
        self.initConnect()
        self.initData()


    def initUI(self):
        self.stackList = QListWidget()

        self.stackList.insertItem(0, '记事本')
        self.stackList.insertItem(1, '计算器')

        self.stack = QStackedWidget(self)

        self.textEditBox = TextEditBox()
        self.stack.addWidget(self.textEditBox)

        self.calcBox = QWidget()
        self.stack.addWidget(self.calcBox)


        layout = QHBoxLayout()
        layout.addWidget(self.stackList)
        layout.addWidget(self.stack)



        self.setLayout(layout)
        self.setGeometry(1000, 300, 900, 700)  # 设置几何形状 参数对应：在桌面的 x,y 和 UI宽，高


    def initData(self):
        pass


    def initConnect(self):
        #self.stackList.itemClicked.connect(self.)
        self.stackList.currentRowChanged.connect(self.display)


    def display(self, i):
        self.stack.setCurrentIndex(i)

if __name__ == '__main__':     
     app = QApplication(sys.argv)
     ui = MainWindow()
     ui.show()
     sys.exit(app.exec_())