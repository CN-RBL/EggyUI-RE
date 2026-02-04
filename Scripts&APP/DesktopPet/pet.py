# -*- coding: utf-8 -*-
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from qfluentwidgets import RoundMenu, Action
from util import get_path

# 桌宠


class EmoticonWidget(QWidget):
    def __init__(self, parent: "Pet" = None):
        super().__init__()
        self.setWindowTitle("Your Eggy - Emoticon")
        self.setWindowIcon(parent.windowIcon())
        self.setWindowFlag(parent.windowFlags())
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(100, 100)

    def set_emoticon(self, emoticon: str) -> None:
        """
        通过此方法设置表情气泡中的表情图片
        :param emoticon: 表情名称
        """
        pass


class TalkWidget(QWidget):
    def __init__(self, parent: "Pet" = None):
        super().__init__()
        self.setWindowTitle("Your Eggy - Talk")
        self.setWindowIcon(parent.windowIcon())
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # TODO: 开发日2：完成界面


class Pet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Eggy")
        self.setWindowIcon(QIcon(get_path(__file__, "icon.ico")))
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(350, 350)

        self.img = QPixmap(get_path(__file__, "imgs/wait.png"))
        self.label = QLabel(self)
        self.label.setPixmap(self.img)
        self.label.setGeometry(0, 0, 350, 350)
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_menu)
        self.label.show()

    def show_menu(self, pos) -> None:
        """
        通过此方法显示右键菜单
        :param pos: 菜单显示位置
        """
        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(text="Talk", triggered=self.talk),
            Action(text="Settings", triggered=self.settings),
            Action(text="Exit", triggered=self.close)])
        menu.exec(self.mapToGlobal(pos))

    def talk(self) -> None:
        """
        通过此方法进入AI讨论页面
        """
        self.talk_win = TalkWidget(parent=self)
        self.talk_win.show()


    def settings(self) -> None:
        # TODO: idea: jump to center
        pass
