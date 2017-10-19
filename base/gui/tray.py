from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers.settings import *


class AppTrayMenu(QMenu):
    exitRequested = pyqtSignal()
    soundsRequested = pyqtSignal(bool)
    animationsRequested = pyqtSignal(bool)
    hotkeyRequested = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        # Mute sounds
        sound_effects = QAction('Enable sounds', self)
        sound_effects.setCheckable(True)
        sound_effects.setChecked(True)
        sound_effects.triggered.connect(self.soundsRequested.emit)
        self.addAction(sound_effects)

        # Animations
        animations = QAction('Animations', self)
        animations.setCheckable(True)
        animations.setChecked(True)
        animations.triggered.connect(self.animationsRequested.emit)
        self.addAction(animations)

        # Global hotkey
        hotkey = QAction('Global hotkey', self)
        hotkey.setCheckable(True)
        hotkey.setChecked(True)
        hotkey.triggered.connect(self.hotkeyRequested.emit)
        self.addAction(hotkey)

        # Preferences
        # TODO
        preferences = QAction('Preferences', self)
        preferences.triggered.connect(lambda: print('heyho'))
        self.addAction(preferences)

        # Separator
        self.addSeparator()

        # Exit the app
        exit_app = QAction('Quit', self)
        exit_app.triggered.connect(self.exitRequested.emit)
        self.addAction(exit_app)


class AppTrayIcon(QSystemTrayIcon):
    visibilityToggleRequested = pyqtSignal()

    def __init__(self, icon):
        super().__init__()

        # Icon
        self.setIcon(icon)

        # Menu
        self.menu = AppTrayMenu()
        self.setContextMenu(self.menu)

        # Triggers
        self.activated.connect(self.toggle)

        # Tooltip
        self.setToolTip('Highlight')

        # Show the icon
        self.show()

    def toggle(self, reason: QSystemTrayIcon.ActivationReason):
        # filter out context calls
        if reason != QSystemTrayIcon.Context:
            self.visibilityToggleRequested.emit()
