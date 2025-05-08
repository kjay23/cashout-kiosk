import os

# Force software rendering and safe Chromium flags
os.environ["QT_OPENGL"] = "software"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

# Optional: Disable Vulkan if available
os.environ["QT_QUICK_BACKEND"] = "software"

import sys
from PyQt6.QtCore import QUrl, Qt, QCoreApplication
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Use software OpenGL
QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 480)
        self.showFullScreen()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:5000"))
        self.setCentralWidget(self.browser)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec())

