from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import keyboard
import signal

from .helpers import settings
from .gui.window import *
from .gui.tray import *
from .gui.preferences import *


class Application(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        # Application icon
        self.appIcon = settings.icon('logo')
        self.setWindowIcon(self.appIcon)

        # Graceful exit
        signal.signal(signal.SIGINT, self.close)
        signal.signal(signal.SIGTERM, self.close)

        # Tray icon
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.trayIcon = AppTrayIcon(self.appIcon)

            # Menu connections
            self.trayIcon.menu.exitRequested.connect(self.close)
            self.trayIcon.menu.soundsToggled.connect(self.sounds_manager)
            self.trayIcon.menu.animationsToggled.connect(self.animation_manager)
            self.trayIcon.menu.hotkeyToggled.connect(self.hotkey_manager)
            self.trayIcon.menu.preferencesRequested.connect(self.open_preferences)

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

        # Decide what screen to use
        if settings.SCREEN_NUM == -1:
            screen = QApplication.desktop().screenNumber(QCursor.pos())
        else:
            screen = settings.SCREEN_NUM

        # Center the window
        desk_geometry = QApplication.desktop().screenGeometry(screen)
        desk_x = desk_geometry.width()
        desk_y = desk_geometry.height()
        self.move(desk_x // 2 - settings.WIDTH // 2 + desk_geometry.left(),
                  desk_y // 2 - (settings.S_FIELD_HEIGHT + settings.RESULTS_HEIGHT) // 2 + desk_geometry.top())

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
        settings.SOUNDS_ENABLED = enabled
        print('Sounds:', enabled)

    # -- Animations
    def animation_manager(self, enabled: bool):
        # TODO settings: turn on/off animations
        settings.ANIMATIONS_ENABLED = enabled
        print('Animations:', enabled)

    # -- Global hotkey
    def hotkey_manager(self, enabled: bool):
        # TODO settings: toggle global hotkey
        settings.GLOBAL_HOTKEY_ENABLED = enabled
        print('Hotkey:', enabled)

        # Global hot key
        keyboard.add_hotkey('ctrl+shift+space', self.toggle_visibility)

    # -- Open Preferences
    def open_preferences(self):
        self.appWidget.searchField.releaseKeyboard()
        pref = PreferencesDialog(self)
        pref.exec()
        self.appWidget.searchField.grabKeyboard()

    # -- Exit application
    def closeEvent(self, event: QCloseEvent):
        # Force sync settings
        settings.sync()

        # If there is a tray icon, remove it
        if self.trayIcon:
            self.trayIcon.hide()

        event.accept()
