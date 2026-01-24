# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from util import get_path

class Pet(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Eggy")
        self.setWindowIcon(QIcon(get_path(__file__, "icon.ico")))
        # self.setWindowFlag(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(350, 350)

    def talk(self):  pass
    def settings(self): pass
    def exit(self):  exit(0)
