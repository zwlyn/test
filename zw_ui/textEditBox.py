import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from log import logger

class TextEditBox(QFrame):
    windowList = []
    def __init__(self):
        super(TextEditBox, self).__init__()

        self.initUI()
        self.initConnect()
        self.initData()


    def initUI(self):
        self.layout = QVBoxLayout()
        self.textEdit = QTextEdit()

        self.createActions()
        self.createMenu()
        self.layout.addWidget(self.textEdit)
        self.statusBar()

        self.setLayout(self.layout)
        self.setGeometry(1000, 300, 800, 700)  # 设置几何形状 参数对应：在桌面的 x,y 和 UI宽，高


    def initData(self):
        pass


    def initConnect(self):
        pass


    def createActions(self):
        self.newAct = QAction('new', self, triggered=self.newWindow)
        self.openAct = QAction('open',self, triggered=self.open)
        self.sayAct = QAction('say', self, triggered=self.say)
        self.exitAct = QAction('exit', triggered=self.close)
        self.saveAsAct = QAction('saveAs', triggered=self.saveAs)


    def createMenu(self):
        menu = QMenuBar()
        self.fileMenu = menu.addMenu('&File')
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.sayAct)
        self.fileMenu.addAction(self.exitAct)
        self.fileMenu.addAction(self.saveAsAct)

        self.layout.addWidget(menu)


    def statusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar.showMessage('statusBar')
        self.layout.addWidget(self.statusBar)


    def newWindow(self):
        another = TextEditBox()
        TextEditBox.windowList.append(another)  # 若不这么做,another的新创建口会被垃圾回收机制回收
        another.show()



    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            file = QFile(fileName)      # 打开文件
            file.open(QFile.ReadOnly)   # 打开方式必须要写！ 不写报 no device的错误

            instr = QTextStream(file)   # 将文件中的str装入QTextStream object

            self.textEdit.setPlainText(instr.readAll())  # 将QTextStream object 中的str流输出到 textEdit
        self.statusBar.showMessage('open:  %s' % fileName, 4000)  # 在状态栏中显示4秒


    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            file = QFile(fileName)
            file.open(QFile.WriteOnly)
            outstr = QTextStream(file)
            outstr << self.textEdit.toPlainText()  # 将textEdit中的str流输出到另存的文件中
            logger.info(outstr)
        self.statusBar.showMessage('File saveAs:  %s' % fileName, 4000)


    def say(self):
        self.textEdit.append('Hello everyone!')

        self.statusBar.showMessage('say Hello everyone!', 3000)


if __name__ == '__main__':     
     app = QApplication(sys.argv)
     ex = TextEditBox()
     ex.show()
     sys.exit(app.exec_())