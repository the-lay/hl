from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers import settings


class PreferencesDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent, flags=Qt.WindowCloseButtonHint | Qt.WindowTitleHint)

        # Dialog settings
        self.setWindowTitle('Current settings')
        self.setSizeGripEnabled(False)

        # Layout
        main_layout = QFormLayout()

        for k in settings.keys():
            name = QLabel(k)
            value = str(settings[k])
            te = QLineEdit(value)

            def on_change(text):
                settings[k] = text

            te.textChanged.connect(on_change)
            main_layout.addRow(name, te)

        self.setLayout(main_layout)
