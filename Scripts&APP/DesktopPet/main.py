# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication
from tray import Tray
from pet import Pet
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = Pet()
    pet.show()
    tray = Tray(parent=pet)
    tray.show()
    app.exec()
