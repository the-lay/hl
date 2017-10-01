from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Search(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        # Frame
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mainLayout.setAlignment(Qt.AlignTop)

        # Search field
        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText('Search')

        # Search field font
        font = self.searchField.font()
        font.setPointSize(27)
        self.searchField.setFont(font)

        # Bottom layout
        self.resultsLayout = QHBoxLayout()

        # Results fields
        self.resultsList = QListView()
        self.resultsLayout.addWidget(self.resultsList)
        self.resultsLayout.setStretch(0, 4)

        # Details field
        self.detailsField = QLabel('adfgadfg')
        self.resultsLayout.addWidget(self.detailsField)
        self.resultsLayout.setStretch(1, 6)

        self.mainLayout.addWidget(self.searchField)
        self.mainLayout.addLayout(self.resultsLayout)
        self.setLayout(self.mainLayout)
