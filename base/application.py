from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import keyboard
import signal

from .helpers import settings
from .gui.window import *
from .gui.tray import *


class Application(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        # Application icon
        self.appIcon = settings.icon('logo')
        self.setWindowIcon(self.appIcon)

        # Graceful exit
        signal.signal(signal.SIGINT, self.close_app)
        signal.signal(signal.SIGTERM, self.close_app)

        # Tray icon
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.trayIcon = AppTrayIcon(self.appIcon)

            # Menu connections
            self.trayIcon.menu.exitRequested.connect(self.close_app)
            self.trayIcon.menu.soundsRequested.connect(self.sounds_manager)
            self.trayIcon.menu.animationsRequested.connect(self.animation_manager)
            self.trayIcon.menu.hotkeyRequested.connect(self.hotkey_manager)

            # Tray click
            self.trayIcon.visibilityToggleRequested.connect(self.toggle_visibility)

        # Escape shortcut
        # TODO maybe move it to hotkey manager?
        shortcut = QShortcut(Qt.Key_Escape, self)
        shortcut.activated.connect(self.hide_app)

        # Central widget
        self.appWidget = AppWidget()
        self.setCentralWidget(self.appWidget)

        # Size
        self.setFixedSize(settings.WIDTH, settings.S_FIELD_HEIGHT)

        # Center the window
        # Take the full (with results) window size
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                            Qt.AlignVCenter | Qt.AlignHCenter,
                                            QSize(settings.WIDTH,
                                                  settings.S_FIELD_HEIGHT + settings.RESULTS_HEIGHT),
                                            qApp.desktop().availableGeometry()))

        # Background color
        # self.setStyleSheet('background-color: {};'.format(settings.BACKGROUND_COLOR))

        # Show app on launch
        # TODO settings: run minimized/open on first launch
        self.show_app()

    # -- Visibility
    def hide_app(self):
        self.hide()

        print('Visible:', self.isVisible())

    def show_app(self):
        # Clear any previous query
        self.appWidget.searchField.setText(None)

        # Show the window
        self.show()
        self.raise_()

        # Focus
        self.activateWindow()
        self.focusWidget()
        self.appWidget.searchField.setFocus()

        print('Visible:', self.isVisible())

    def toggle_visibility(self):
        if self.isVisible():
            self.hide_app()
        else:
            self.show_app()

    # -- Sounds
    def sounds_manager(self, enabled: bool):
        # TODO typing sounds? search finished ding? probably bad idea
        print('Sounds:', enabled)

    # -- Animations
    def animation_manager(self, enabled: bool):
        # TODO settings: turn on/off animations
        print('Animations:', enabled)

    # -- Global hotkey
    def hotkey_manager(self, enabled: bool):
        # TODO settings: toggle global hotkey
        print('Hotkey:', enabled)

        # Global hot key
        # keyboard.add_hotkey('shift+space', self.toggle_visibility)

    # -- Exit application
    def closeEvent(self, event: QCloseEvent):
        # Force sync settings
        settings.qsettings.sync()

        # If there is a tray icon, remove it
        if self.trayIcon:
            self.trayIcon.hide()

        event.accept()

    def close_app(self):
        # Close the app
        qApp.quit()
