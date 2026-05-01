# -*- coding: utf-8 -*-

import platform
import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QSizePolicy, QListWidgetItem, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QMessageBox
from qfluentwidgets import *
import subprocess

# import requests

__version__ = "vRE 1.0.0.Beta"


class MainWindow(MSFluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("EggyUI Center-Plugin Maker")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setMinimumSize(QSize(800, 600))
        setThemeColor(QColor("#fed71d"))
        self.initUI()

    def initUI(self):
        self.addSubInterface(MainInterface(), FluentIcon("Home"), "首页")
        self.addSubInterface(CodingInterface(), FluentIcon("Code"), "代码")
        self.addSubInterface(TutorialInterface(), FluentIcon("BookShelf"), "教程")
        self.addSubInterface(FeedbackInterface(), FluentIcon("Feedback"), "反馈",
                             position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(SettingInterface(), FluentIcon("Setting"), "设置",
                             position=NavigationItemPosition.BOTTOM)


class MainInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainInterface")
        self.initInterface()

    def initInterface(self):
        mainLayout = VBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)


class CodingInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("CodingInterface")

        self.initInterface()

    def initInterface(self):
        mainLayout = VBoxLayout(self)


        self.setLayout(mainLayout)


class TutorialInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("TutorialInterface")

        self.initInterface()

    def initInterface(self):
        mainLayout = VBoxLayout(self)


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
        mainLayout = VBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        theme_setcard = OptionsSettingCard(
            qconfig.themeMode,
            FluentIcon.BRUSH,
            "应用主题",
            "调整你的应用外观",
            texts=["浅色", "深色", "跟随系统设置"],
            parent=self
        )
        updatecard = PushSettingCard(
            "检测更新",
            FluentIcon.UPDATE,
            "检测更新",
            "检测EggyUI Center-Plugin Maker的更新",
            self
        )
        updatecard.button.clicked.connect(lambda: print("Hi"))
        helpcard = HyperlinkCard(
            url="https://eggyui.mysxl.cn/eggyui",
            text="打开EggyUI官网",
            icon=FluentIcon.HELP,
            title="帮助",
            content="关于EggyUI(-RE)的内容",
            parent=self
        )

        mainLayout.addWidget(theme_setcard)
        mainLayout.addWidget(updatecard)
        mainLayout.addWidget(helpcard)
        theme_setcard.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "nul",
             "--connect-timeout", str(2), "-w", "%{http_code}", "www.baidu.com"],
            capture_output=True, text=True, timeout=5
        )
        http_code = result.stdout.strip()
        if http_code.isdigit() and int(http_code) == 200:
            print(f"网络连通，HTTP 状态码: {http_code}")
        else:
            raise Exception
    except:
        err_box = QMessageBox.information(None, "Eggy UI Center-Plugin Maker", "本组件需要联网，请检查网络连接并重启组件！")
    win.show()
    app.exec()
