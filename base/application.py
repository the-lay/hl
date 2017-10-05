from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import keyboard

from .helpers.settings import *
from .gui.window import *
from .gui.tray import *


class Application(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        # Icon
        self.appIcon = QIcon()
        icon_path = str(AppSettings.get_resource('', 'logo.png'))
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
            self.trayIcon.menu.animationsRequested.connect(self.animation_manager)
            self.trayIcon.visibilityToggleRequested.connect(self.toggle_visibility)

        # Escape shortcut
        shortcut = QShortcut(Qt.Key_Escape, self)
        shortcut.activated.connect(self.hide_app)

        # Global hot key
        # keyboard.add_hotkey('shift+space', self.toggle_visibility)

        # GUI
        # self.setAttribute(Qt.WA_NoSystemBackground)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAttribute(Qt.WA_PaintOnScreen)

        # Central widget
        self.appWidget = AppWidget()
        self.setCentralWidget(self.appWidget)

        # Size
        self.setFixedSize(AppSettings.WIDTH, AppSettings.S_FIELD_HEIGHT)

        # Center the window
        # Take the full (with results) window size
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                            Qt.AlignVCenter | Qt.AlignHCenter,
                                            QSize(AppSettings.WIDTH,
                                                  AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT),
                                            qApp.desktop().availableGeometry()))

        # Show app on launch
        # TODO settings: run minimized/open on first launch
        self.show_app()

    # -- Visibility
    def hide_app(self):
        self.hide()

        print('Visible: ', self.isVisible())

    def show_app(self):
        self.show()
        self.raise_()
        self.activateWindow()
        self.focusWidget()
        self.appWidget.searchField.setText(None)
        self.appWidget.searchField.setFocus()

        print('Visible: ', self.isVisible())

    def toggle_visibility(self):
        if self.isVisible():
            self.hide_app()
        else:
            self.show_app()

    # -- Sounds
    def sounds_manager(self, enabled: bool):
        # TODO typing sounds? search finished ding? probably bad idea
        print('Sounds: ', enabled)

    # -- Animations
    def animation_manager(self, enabled: bool):
        # TODO settings: turn on/off animations
        print('Animations: ', enabled)

    # -- Exit application
    def close_app(self):
        # If there is a tray icon, remove it
        if self.trayIcon:
            self.trayIcon.hide()

        # Close the app
        qApp.quit()
