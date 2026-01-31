# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QSystemTrayIcon, QWidget
from PyQt6.QtGui import QIcon
from qfluentwidgets import SystemTrayMenu, Action

class Tray(QSystemTrayIcon):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action("Show/Hide", triggered=self.switchVisibility),
            Action("Talk", triggered=parent.talk),  # 与Pet交流（互动？）
            Action("Settings", triggered=parent.settings),
            Action("Exit", triggered=parent.exit)
        ])

        self.setContextMenu(self.menu)
    
    def switchVisibility(self):
        if self.parent().isVisible():
            self.parent().hide()
        else:
            self.parent().show()