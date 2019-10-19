import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MyUI(QMainWindow):
    sequenceNumber = 1
    windowList = []
    def __init__(self, fileName=None):
        super(MyUI,self).__init__()
        self.initData()
        self.initUI()
        self.initConnect()

        if fileName:
            self.loadFile(fileName)
        else:
            self.setCurrentFile(self.curFile)

    def initData(self):
        self.curFile = None
    def initUI(self):
        self.isUntitled = True

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('QMainWindow综合使用')

    def createActions(self):
        self.exitAct = QAction(QIcon('img/1.png'), 'Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('退出程序')
        self.exitAct.triggered.connect(self.close)

        self.saveAct = QAction(QIcon('images/save.png'), "&Save", self,
            shortcut=QKeySequence.Save,
            statusTip="Save the document to disk", triggered=self.save)

        self.openAct = QAction(QIcon('images/open.png'), "&Open", self,
            shortcut=QKeySequence.Open, statusTip="Open an existing file",
            triggered=self.open)

        self.saveAsAct = QAction(QIcon('images/saveAs.png'), "&SaveAs", self,
            shortcut=QKeySequence.SaveAs,
            statusTip="Save the document under a new name",
            triggered=self.saveAs)

    def createMenus(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        self.fileMenu = menubar.addMenu('File')
        self.fileMenu.addAction(self.exitAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)


    def createToolBars(self):
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.exitAct)
        toolbar.addAction(self.openAct)
        toolbar.addAction(self.saveAct)
        toolbar.addAction(self.saveAsAct)


    def createStatusBar(self):
        self.statusBar().showMessage('状态栏看我')
    def initConnect(self):
        pass

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ =QFileDialog.getSaveFileName(self, "Save As",
            self.curFile)
        if not fileName:
            return False
        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "SDI",
                "Cannot write file %s :\n%s." % (fileName,file.errorString()))
            return False
        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage('File saved', 2000)
        return True


    def setCurrentFile(self, fileName):
        self.isUntitled = not fileName   # 若文件已经命名 则为False
        if self.isUntitled:
            self.curFile = "document%d.txt" % MyUI.sequenceNumber
            MyUI.sequenceNumber += 1
        else:
            self.curFile = QFileInfo(fileName).canonicalFilePath()

        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        self.setWindowTitle("%s[*] - SDI" % self.strippedName(self.curFile))
        
    def strippedName(self,fullFileName):
        return QFileInfo(fullFileName).fileName()

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "SDI",
                "Cannot read file %s:\n%s." % (fileName, file.errorString()))

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage('File loaded', 2000)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMainWindow(fileName)
            if existing:
                existing.show()
                existing.raise_()
                existing.activateWindow()
                return
            if self.isUntitled and self.textEdit.document().isEmpty() and not self.isWindowModified():
                 self.loadFile(fileName)
            else:
                other = MyUI(fileName)
                if other.isUntitled:
                    del other
                    return

                MyUI.windowList.append(other)
                other.move(self.x() + 40, self.y() + 40)
                other.show()

    def findMainWindow(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for widget in QApplication.instance().topLevelWidgets():
            if isinstance(widget, MyUI) and widget.curFile == canonicalFilePath:
                return widget

        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MyUI()
    ui.show()
    sys.exit(app.exec_())
