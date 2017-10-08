from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from base.helpers.settings import AppSettings


class ResultsWidget(QWidget):

    def __init__(self):
        super().__init__()

        # Main layout
        self.mainLayout = QHBoxLayout()
        # self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setContentsMargins(QMargins(1, 0, 1, 5))

        self.setFixedSize(AppSettings.WIDTH, AppSettings.RESULTS_HEIGHT)

        # Results fields
        self.resultsList = QListView()
        self.resultsList.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.resultsList)
        self.mainLayout.setStretch(0, 4)

        # Details field
        self.detailsField = QLabel('Results go here')
        self.mainLayout.addWidget(self.detailsField)
        self.mainLayout.setStretch(1, 6)

        self.setLayout(self.mainLayout)

    def search(self, field: str):
        self.detailsField.setText(field)
