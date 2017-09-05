from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import keyboard

from .helpers.settings import *
from .gui.search import *
from .gui.tray import *


class Application(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.Tool | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        # Icon
        self.appIcon = QIcon()
        icon_path = str(AppSettings.get_resource('logo.png'))
        self.appIcon.addFile(icon_path, QSize(16, 16))
        self.appIcon.addFile(icon_path, QSize(24, 24))
        self.appIcon.addFile(icon_path, QSize(32, 32))
        self.appIcon.addFile(icon_path, QSize(48, 48))
        self.appIcon.addFile(icon_path, QSize(256, 256))
        self.appIcon.addFile(icon_path, QSize(512, 512))
        self.setWindowIcon(QIcon(self.appIcon))

        # Tray icon
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.trayIcon = AppTrayIcon(self.appIcon)
            # Connections
            self.trayIcon.menu.exitRequested.connect(self.close_app)
            self.trayIcon.menu.soundsRequested.connect(self.sounds_manager)
            self.trayIcon.visibilityToggleRequested.connect(self.toggle_visibility)

        # Global keyboard hot key
        keyboard.add_hotkey('ctrl+space', self.toggle_visibility)

        # Central widget
        self.appWidget = AppWidget()
        self.setCentralWidget(self.appWidget)

    # Visibility
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.setFocus()

    # Sounds
    def sounds_manager(self, enabled: bool):
        # TODO
        print('adfgadfg', enabled)

    # Method is called to safely shut down the app
    def close_app(self):
        # If there is a tray icon, remove it
        if self.trayIcon:
            self.trayIcon.hide()

        # Close the app
        qApp.quit()
