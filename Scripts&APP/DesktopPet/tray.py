# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QSystemTrayIcon
from qfluentwidgets import SystemTrayMenu, Action
from pet import Pet


class Tray(QSystemTrayIcon):
    def __init__(self, parent: Pet = None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action(text="Show/Hide", triggered=self.switchVisibility),
            Action(text="Talk", triggered=parent.talk),  # 与Pet交流（互动？）
            Action(text="Settings", triggered=parent.settings),
            Action(text="Exit", triggered=parent.close)
        ])

        self.setContextMenu(self.menu)

    def switchVisibility(self):
        if self.parent().isVisible():
            self.parent().hide()
        else:
            self.parent().show()
