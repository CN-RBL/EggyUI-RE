# -*- coding: utf-8 -*-
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QSizePolicy, QListWidgetItem
from qfluentwidgets import *
import requests


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
        self.addSubInterface(GloPMInterface(), FluentIcon("Application"), "GLO PM")
        self.addSubInterface(FeedbackInterface(), FluentIcon("Feedback"), "Feedback",
                             position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(SettingInterface(), FluentIcon("Setting"), "Setting",
                             position=NavigationItemPosition.BOTTOM)


class MainInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainInterface")
        self.initInterface()

    def initInterface(self):
        mainLayout = VBoxLayout(self)
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


class GloPMInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("GLO_PMInterface")

        self.initInterface()

    def initInterface(self):
        mainLayout = VBoxLayout(self)

        kit_list = ListWidget(self)

        class KitDownloadItem(QListWidgetItem):
            def __init__(self, text):
                super().__init__(text)

            def paint(self, painter, option, index):
                painter.drawRect(option.rect)
                painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, self.text())

        kit_list.addItem(KitDownloadItem("Eggy Desktop Pet"))
        kit_list.addItem(KitDownloadItem("But"))
        kit_list.addItem(KitDownloadItem("NeedMore!EggyKit!"))
        kit_list.sortItems(order=Qt.SortOrder.AscendingOrder)
        kit_list.show()
        mainLayout.addWidget(kit_list)


class FeedbackInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("FeedbackInterface")

        self.initInterface()

    def initInterface(self):
        mainLayout = VBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = BodyLabel()
        title_label.setText("标题")
        mainLayout.addWidget(title_label)

        title_input = TextEdit(self)
        mainLayout.addWidget(title_input)


class SettingInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("SettingInterface")

        self.initInterface()

    def initInterface(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
