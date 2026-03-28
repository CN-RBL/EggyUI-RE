import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QContextMenuEvent


# 自定义 WebEngineView，禁用右键菜单
class CustomWebEngineView(QWebEngineView):
    def contextMenuEvent(self, event: QContextMenuEvent):
        # 完全忽略右键菜单事件
        event.accept()


class LocalWebApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EggyUI-RE 1.0 Installer")
        self.setFixedSize(700, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMinMaxButtonsHint)

        # 隐藏默认菜单栏
        self.menuBar().setVisible(False)

        # 创建中央 widget 和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 去除布局的边距和间距，使 Web 视图完全填充窗口
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建自定义 Web 引擎视图（已禁用右键菜单）
        self.web_view = CustomWebEngineView()

        # 加载同目录下的 interface.html
        self.load_interface_html()

        # 将 Web 视图添加到布局
        layout.addWidget(self.web_view)

    def load_interface_html(self):
        """加载程序所在目录下的 interface.html 文件"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "interface.html")
        url = QUrl.fromLocalFile(html_path)
        self.web_view.load(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LocalWebApp()
    window.show()
    sys.exit(app.exec())
