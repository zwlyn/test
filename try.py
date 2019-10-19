import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MyUI(QMainWindow):
    def __init__(self, fileName=None):
        super(MyUI,self).__init__()
        self.lineEdit_int = QLineEdit()
        self.initData()
        self.initUI()
        self.initConnect()

    def initData(self):
        pass
    def initUI(self):
        self.initAction()

        self.initMenuBar()
        self.initToolBar()
        self.initCentralWidget()
        self.initStatusBar()


        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Windows')

    def initAction(self):
        self.displayAct = QAction(QIcon('img/ball.png'), 'display', self, triggered=self.display,
                                  statusTip="Let 's display!!")
        self.exitAct = QAction(QIcon('img/1.png'), 'Exit', self, triggered=self.close,
                               statusTip="exit!!")
        self.saveAct = QAction(QIcon('images/save.png'),'save', statusTip='save', triggered=self.save)

    def initMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(self.displayAct)
        fileMenu.addAction(self.exitAct)
        fileMenu.addAction(self.saveAct)

    def initStatusBar(self):
        self.statusBar().showMessage('Hi man!')

    def initToolBar(self):
        self.toolBar = self.addToolBar("")
        self.toolBar.addAction(self.exitAct)
        self.toolBar.addAction(self.displayAct)
        self.toolBar.addAction(self.saveAct)

    def initCentralWidget(self):
        mainWidget = QWidget()
        layout = QFormLayout()
        self.lineEdit_int.setValidator(QIntValidator())  # validator 验证器
        label1 = QLabel('age: ')
        layout.addRow(label1,self.lineEdit_int)
        layout.addRow(QLabel('22'),QLineEdit())
        layout.addRow(QLabel('33'),QLineEdit())
        layout.addRow(QLabel('44'),QLineEdit())
        layout.addRow(QLabel('55'),QLineEdit())
        self.textEdit = QTextEdit()
        btn_add = QPushButton('添加文本')
        btn_clear = QPushButton('清除文本')

        btn_add.clicked.connect(self.add)
        btn_clear.clicked.connect(self.clear)
        layout.addRow(self.textEdit)
        layout.addRow(btn_add)
        layout.addRow(btn_clear)
        mainWidget.setLayout(layout)

        self.setCentralWidget(mainWidget)
    def initConnect(self):
        pass

    def add(self):
        self.textEdit.append('666')
        self.statusBar().showMessage('添加文本', 2000)  # 2000用于显示两秒

    def clear(self):
        self.textEdit.clear()
        self.statusBar().showMessage('清除文本')

    def display(self):
        QMessageBox.warning(self, 'sward', 'zw miss lyn every day!')
        print('zw love Lyn!')

    def save(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save",
            '')

        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "SDI",
                "Cannot write file %s :\n%s." % (fileName,file.errorString()))
            return False
        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage('File saved', 2000)
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyUI()
    ui.show()
    sys.exit(app.exec_())
