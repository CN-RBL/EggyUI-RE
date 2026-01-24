# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from util import get_path

class Emoticon_Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(100, 100)
    
    def set_emoticon(self, emoticon_path: str):
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

    def talk(self):
        """
        通过此方法进入AI讨论页面
        """
        pass
    def settings(self): pass
    def exit(self):
        exit()
