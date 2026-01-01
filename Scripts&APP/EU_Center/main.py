# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame
from qfluentwidgets import *


class MainWindow(MSFluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EggyUI-RE Center")

        self.initUI()

    def initUI(self):
        self.addSubInterface(MainInterface(), FluentIcon("Home"), "Home")


class MainInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainInterface")

        self.initInterface()

    def initInterface(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()

