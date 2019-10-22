import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from log import logger


class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expending, QSizePolicy.Preferred) 
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size


class calcBox(QFrame):
    NumDigitButtons = 10
    def __init__(self, parent=None):
        super(calcBox, self).__init__(parent)
        self.initData()
        self.initUI()
        self.initConnect()



    def initUI(self):
        # 创建显示屏
        
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)

        # 创建数字按钮
        self.digitButtons = []

        for i in range(calcBox.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i),
                        self.digitClicked))

        self.setLayout(layout)
        self.setGeometry(1000, 300, 900, 700)  # 设置几何形状 参数对应：在桌面的 x,y 和 UI宽，高


    def initData(self):
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''

    def initConnect(self):
        pass

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())

        if self.display.text() == '0' and digitValue == 0.0:
            return

        if self.waitingForOperand:
            self.display.cear()
            self.waitingForOperand =False

        self.display.setText(self.display.text() + str(digitValue))

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button


if __name__ == '__main__':     
     app = QApplication(sys.argv)
     ui = calcBox()
     ui.show()
     sys.exit(app.exec_())