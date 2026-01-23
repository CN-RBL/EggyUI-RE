# -*- coding: utf-8 -*-

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QSystemTrayIcon
from qfluentwidgets import SystemTrayMenu

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent: QtWidgets.QWidget=None):
        super().__init__(parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent)
