from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers.settings import *


class AppTrayMenu(QMenu):
    exitRequested = pyqtSignal()
    soundsRequested = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        # Mute sounds
        sound_effects = QAction('Enable sounds', self)
        sound_effects.setCheckable(True)
        sound_effects.setChecked(True)
        sound_effects.triggered.connect(self.soundsRequested.emit)
        self.addAction(sound_effects)

        # Separator
        self.addSeparator()

        # Exit the app
        exit_app = QAction('Quit the application', self)
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
