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

        # Search timer, for search delay
        # https://ux.stackexchange.com/questions/34360/delay-on-keystroke-when-search-as-you-type
        self.searchTimer = QTimer(self)
        self.searchTimer.setSingleShot(True)
        self.searchTimer.timeout.connect(self.do_query)

        # Results widget
        # Results widget is being added/hidden depending on text input, hide it initially
        self.resultsWidget = ResultsWidget()
        self.resultsWidget.setVisible(False)
        self.resultsOpen = False  # can't trust QWidget.isVisible with animations

        # Register search field and layout
        self.mainLayout.addWidget(self.searchField)
        self.mainLayout.addWidget(self.resultsWidget)
        self.setLayout(self.mainLayout)

        # Connections
        self.searchField.textChanged.connect(self.text_input)

    # Triggered upon change in search field
    # Handles results widget toggling and delaying search query
    def text_input(self, field: str):

        # Results widget opening/closing
        if not field:

            # Hide results widget
            self.resultsWidget.setVisible(False)

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

            # Stop executing further
            return

        # Ignore if last character is a blank space
        if field.endswith(' '):
            return

        # If results widget is not seen, open it
        if not self.resultsOpen:

            # Set maximum height, animate minimum
            self.parent().setMaximumHeight(AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT)

            a = QPropertyAnimation(self.parent(), b'minimumHeight')
            a.setDuration(AppSettings.ANIMATION_DURATION)
            a.setStartValue(AppSettings.S_FIELD_HEIGHT)
            a.setEndValue(AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT)
            a.setEasingCurve(QEasingCurve.OutBack)
            a.start(QPropertyAnimation.DeleteWhenStopped)

            # Show results widget on animation finish
            a.finished.connect(lambda: self.resultsWidget.setVisible(True))

            # Need to keep reference, otherwise gets GC'ed immediately
            self.resultsWidget.animation = a

            # Set flag
            self.resultsOpen = True

        # Add a delay on search
        self.searchTimer.start(AppSettings.SEARCH_DELAY)

    # Assume user stopped typing, start searching
    def do_query(self):
        # TODO Intermediate point, might be useful later to filter or do something, but now kind of pointless
        self.resultsWidget.search(self.searchField.text())
        print('Searching for', self.searchField.text())

