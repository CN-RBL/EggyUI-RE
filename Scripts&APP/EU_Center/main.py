# -*- coding: utf-8 -*-
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QSizePolicy
from qfluentwidgets import *


class MainWindow(MSFluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EggyUI-RE Center")
        self.setWindowIcon(QIcon("icon.png"))
        self.setMinimumSize(QSize(800, 600))
        setThemeColor(QColor("#fed71d"))
        self.initUI()

    def initUI(self):
        self.addSubInterface(MainInterface(), FluentIcon("Home"), "Home")
        self.addSubInterface(GLO_PMInterface(), FluentIcon("Application"), "GLO_PM")
        self.addSubInterface(FeedbackInterface(), FluentIcon("Feedback"), "Feedback", position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(SettingInterface(), FluentIcon("Setting"), "Setting", position=NavigationItemPosition.BOTTOM)


class MainInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainInterface")
        self.initInterface()

    def initInterface(self):
        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        news_c = HeaderCardWidget(self)
        news_c.setTitle("News")
        no_news_l = BodyLabel(news_c)
        no_news_l.setText("No News")
        news_c.viewLayout.addWidget(no_news_l)
        news_c.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        mainLayout.addWidget(news_c)

        info_c = HeaderCardWidget(self)
        info_c.setTitle("Info")
        no_info_l = BodyLabel(info_c)
        no_info_l.setText("No Info")
        info_c.viewLayout.addWidget(no_info_l)
        info_c.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        mainLayout.addWidget(info_c)


class GLO_PMInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("GLO_PMInterface")

    def initInterface(self):
        pass


class FeedbackInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("FeedbackInterface")

        self.initInterface()

    def initInterface(self):
        pass


class SettingInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("SettingInterface")

    def initInterface(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
