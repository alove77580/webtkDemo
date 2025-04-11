import sys
import socket
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl, QTimer, QStandardPaths, Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QPixmap
from datetime import datetime

def check_network_connection():
    try:
        # 尝试连接到一个可靠的网站
        socket.create_connection(("www.baidu.com", 80), timeout=2)
        return True
    except OSError:
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("本地AI问小白 - 网络状态：检查中...")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置Cookie存储路径
        data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        cookie_path = os.path.join(data_path, "cookies")
        os.makedirs(cookie_path, exist_ok=True)
        
        # 创建Web视图和配置文件
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        profile.setPersistentStoragePath(cookie_path)
        
        # 创建主窗口部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建截图按钮
        self.screenshot_button = QPushButton("截图")
        self.screenshot_button.clicked.connect(self.take_screenshot)
        layout.addWidget(self.screenshot_button)
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # 加载目标网站
        self.web_view.setUrl(QUrl("https://www.wenxiaobai.com/"))
        
        # 创建定时器检查网络状态
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_network_status)
        self.timer.start(5000)  # 每5秒检查一次
        
        # 立即检查一次网络状态
        self.update_network_status()
        
        # 添加快捷键
        self.shortcut = QShortcut(QKeySequence("Ctrl+Alt+S"), self)
        self.shortcut.activated.connect(self.take_screenshot)
    
    def take_screenshot(self):
        # 创建截图保存目录
        screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "问小白截图")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # 生成文件名（使用时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(screenshots_dir, f"截图_{timestamp}.png")
        
        # 获取网页内容并保存为图片
        self.web_view.grab().save(filename)
        
        # 显示成功消息
        QMessageBox.information(self, "截图成功", f"截图已保存到：\n{filename}")
    
    def update_network_status(self):
        if check_network_connection():
            self.setWindowTitle("本地AI问小白 - 网络状态：已连接")
        else:
            self.setWindowTitle("本地AI问小白 - 网络状态：未连接")

def main():
    app = QApplication(sys.argv)
    
    # 检查网络连接
    if not check_network_connection():
        QMessageBox.critical(None, "网络错误", "请连接网络后再启动软件")
        sys.exit(1)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()