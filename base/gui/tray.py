from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers import settings


class AppTrayMenu(QMenu):
    exitRequested = pyqtSignal()
    soundsToggled = pyqtSignal(bool)
    animationsToggled = pyqtSignal(bool)
    hotkeyToggled = pyqtSignal(bool)
    preferencesRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Mute sounds
        sound_effects = QAction('Enable sounds', self)
        sound_effects.setCheckable(True)
        sound_effects.setChecked(settings.SOUNDS_ENABLED)
        sound_effects.triggered.connect(self.soundsToggled.emit)
        self.addAction(sound_effects)

        # Animations
        animations = QAction('Animations', self)
        animations.setCheckable(True)
        animations.setChecked(settings.ANIMATIONS_ENABLED)
        animations.triggered.connect(self.animationsToggled.emit)
        self.addAction(animations)

        # Global hotkey
        hotkey = QAction('Global hotkey', self)
        hotkey.setCheckable(True)
        hotkey.setChecked(settings.GLOBAL_HOTKEY_ENABLED)
        hotkey.triggered.connect(self.hotkeyToggled.emit)
        self.addAction(hotkey)

        # Preferences
        preferences = QAction('Preferences', self)
        preferences.triggered.connect(self.preferencesRequested.emit)
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
