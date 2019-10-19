# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QThread
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(515, 208)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setGeometry(QtCore.QRect(280, 150, 92, 28))
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.pushButton_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Stop.setGeometry(QtCore.QRect(390, 150, 92, 28))
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 50, 381, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Start.setText(_translate("MainWindow", "开始"))
        self.pushButton_Stop.setText(_translate("MainWindow", "停止"))
        self.label.setText(_translate("MainWindow", "0"))



class Work(QObject):
    count = int(0)
    count_signal = pyqtSignal(int)

    def __init__(self):
        super(Work, self).__init__()
        self.run = True

    def work(self):
        self.run = True
        while self.run:
            print(str(self.count))
            self.count += 1
            self.count_signal.emit(self.count)
            time.sleep(1)

    def work_stop(self):
        self.run = False


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.pushButton_Start.clicked.connect(self.workStart)
        self.pushButton_Stop.clicked.connect(self.workStop)

        self.thread = QThread()
        self.worker = Work()
        self.worker.count_signal.connect(self.flush)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.thread.finished.connect(self.finished)

    def flush(self, count):
        self.label.setText(str(count))

    def workStart(self):
        print('button start.')
        self.pushButton_Start.setEnabled(False)
        self.thread.start()

    def workStop(self):
        print('button stop.')
        self.worker.work_stop()
        self.thread.quit()

    def finished(self):
        print('finish.')
        self.pushButton_Start.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())





