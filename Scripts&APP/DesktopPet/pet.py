# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from qfluentwidgets import RoundMenu, Action
from util import get_path


class Emoticon_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(100, 100)

    def set_emoticon(self, emoticon_path: str) -> None:
        """
        通过此方法设置表情气泡中的表情图片
        :param emoticon_path: 表情图片路径
        """
        pass


class Pet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Eggy")
        self.setWindowIcon(QIcon(get_path(__file__, "icon.ico")))
        self.setWindowFlag(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(350, 350)

        self.img = QPixmap(get_path(__file__, "imgs/wait.png"))
        self.label = QLabel(self)
        self.label.setPixmap(self.img)
        self.label.setGeometry(0, 0, 350, 350)
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_menu)
        self.label.show()
        # self.setCentralWidget(self.label)

    def show_menu(self, pos) -> None:
        """
        通过此方法显示右键菜单
        :param pos: 菜单显示位置
        """
        menu = RoundMenu(parent=self)
        menu.addActions([
            Action("Talk", triggered=self.talk),
            Action("Settings", triggered=self.settings),
            Action("Exit", triggered=self.exit)])
        menu.exec(self.mapToGlobal(pos))

    def talk(self) -> None:
        """
        通过此方法进入AI讨论页面
        """
        pass

    def settings(self) -> None:
        pass

    def exit(self) -> None:
        self.close()
