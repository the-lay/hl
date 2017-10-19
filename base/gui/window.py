from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..helpers.settings import *


class SearchField(QLineEdit):

    def __init__(self):
        super().__init__()

        # Placeholder
        self.setPlaceholderText('Search')
        # TODO placeholder with typewriter animation of some fun stuff

        # Font
        self.fontSize = 14
        f = self.font()
        f.setPointSize(self.fontSize)
        f.setWeight(QFont.Light)
        self.setFont(f)
        f_metric = QFontMetrics(f)

        # Icon
        self.iconSize = int(f_metric.ascent() / 1.1)
        self.icon = QIcon(str(AppSettings.get_resource('icons', 'search.png')))
        self.setTextMargins(QMargins(self.iconSize + 13, 0, 0, 0))

        # Border
        self.setStyleSheet('border: none; /*border-radius: 5px;*/')
        # TODO borders visible only with translucent background, do I need em?

        # Sizes
        self.setFixedSize(AppSettings.WIDTH, AppSettings.S_FIELD_HEIGHT)

    # Overloading to draw an icon
    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)

        # TODO expose in settings whether to draw icon or not
        # Search icon in the field
        painter = QPainter(self)
        icon_pixmap = self.icon.pixmap(QSize(self.iconSize, self.iconSize))
        painter.drawPixmap(8, (self.height() - self.iconSize) // 2, icon_pixmap)


class ResultsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.mainLayout = QHBoxLayout()
        # self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setContentsMargins(QMargins(1, 0, 1, 5))

        self.setFixedSize(AppSettings.WIDTH, AppSettings.RESULTS_HEIGHT)

        # Results fields
        self.resultsList = QListWidget()
        self.resultsList.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.resultsList)
        self.mainLayout.setStretch(0, 4)

        for i in range(10):
            item = QListWidgetItem("Item %i" % i)
            self.resultsList.addItem(item)

        self.resultsList.setResizeMode(QListView.Adjust)
        self.resultsList.setSpacing(2)

        # Details field
        self.detailsField = QLabel('Results go here')
        self.mainLayout.addWidget(self.detailsField)
        self.mainLayout.setStretch(1, 6)

        self.setLayout(self.mainLayout)

    def search(self, field: str):
        self.detailsField.setText(field)


class FoundItem(QWidget):
    # confidence allows sorting
    # provider allows to traceback

    def __init__(self, confidence: int, provider: int, parent=None):
        super(FoundItem, self).__init__(parent)


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
            self.roll_up()

            # Reset flag
            self.resultsOpen = False

            # Stop executing further
            return

        # Ignore if last character is a blank space
        elif field.endswith(' '):
            return

        # If results widget is not seen, open it
        if not self.resultsOpen:
            # Roll the window
            self.roll_down()

            # Set flag
            self.resultsOpen = True

        # Add a delay on search
        self.searchTimer.start(AppSettings.SEARCH_DELAY)

    # Roll window down
    def roll_down(self):
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

    # Roll window up
    def roll_up(self):
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

        # Remove border
        # self.searchField.setStyleSheet('border: none;')

    # Assume user stopped typing, start searching
    def do_query(self):
        # TODO Intermediate point, might be useful later to filter or do something, but now kind of pointless
        self.resultsWidget.search(self.searchField.text())
        print('Searching for', self.searchField.text())

