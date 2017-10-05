from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .searchfield import *
from .results import *


class AppWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        # Frame
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.mainLayout.setAlignment(Qt.AlignTop)

        # Search field
        self.searchField = SearchField()

        # Register search field and layout
        self.mainLayout.addWidget(self.searchField)
        self.setLayout(self.mainLayout)

        # Results widget
        # Results widget is being added/hidden depending on text input
        self.resultsWidget = ResultsWidget()
        self.resultsOpen = False  # can't trust QWidget.isVisible when animated

        # Connections
        self.searchField.textChanged.connect(self.text_input)

    # Triggered upon change in search field
    def text_input(self, field: str):

        if not field:

            # Hide results widget
            self.resultsWidget.setParent(None)
            self.repaint()

            # Set minimum height, animate maximum height
            self.parent().setMinimumHeight(AppSettings.S_FIELD_HEIGHT)

            a = QPropertyAnimation(self.parent(), b'maximumHeight')
            a.setDuration(AppSettings.ANIMATION_DURATION)
            a.setStartValue(AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT)
            a.setEndValue(AppSettings.S_FIELD_HEIGHT)
            a.setEasingCurve(QEasingCurve.OutBack)
            a.start(QPropertyAnimation.DeleteWhenStopped)

            # Need to keep reference, otherwise gets GC'ed immediately
            self.resultsWidget.animation = a

            # Reset flag
            self.resultsOpen = False

        else:

            # Add results widget
            self.layout().addWidget(self.resultsWidget)

            # Set maximum height, animate minimum
            self.parent().setMaximumHeight(AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT)

            # Prevent from running multiple times
            if not self.resultsOpen:

                a = QPropertyAnimation(self.parent(), b'minimumHeight')
                a.setDuration(AppSettings.ANIMATION_DURATION)
                a.setStartValue(AppSettings.S_FIELD_HEIGHT)
                a.setEndValue(AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT)
                a.setEasingCurve(QEasingCurve.OutBack)
                a.start(QPropertyAnimation.DeleteWhenStopped)

                # Need to keep reference, otherwise gets GC'ed immediately
                self.resultsWidget.animation = a

                # Set flag
                self.resultsOpen = True
