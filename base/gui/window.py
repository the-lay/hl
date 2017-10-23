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
        # TODO when query is processed change icon to something informative?
        self.iconSize = int(f_metric.ascent() * 1.3)
        self.icon = QIcon(str(AppSettings.get_resource('icons', 'search.png')))
        self.setTextMargins(QMargins(self.iconSize + 13, 5, 0, 5))

        # Border
        self.setStyleSheet('border: none; background-color: {}'.format(AppSettings.BACKGROUND_COLOR))

    # Overloading to draw an icon
    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)

        # TODO: expose in settings whether to draw icon or not
        # Search icon in the field
        painter = QPainter(self)
        icon_pixmap = self.icon.pixmap(QSize(self.iconSize, self.iconSize))
        painter.drawPixmap(8, (self.height() - self.iconSize + 5) // 2, icon_pixmap)

    # Handling down/up button TODO: maybe modify tab too?
    def keyPressEvent(self, event: QKeyEvent):
        # TODO: proper button handling
        if event.key() == Qt.Key_Down:
            print('going down in results list')
        elif event.key() == Qt.Key_Up:
            print('going up in results list')
        else:
            super().keyPressEvent(event)


class ResultsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setAlignment(Qt.AlignTop)

        # Separator
        self.hline = QFrame()
        self.hline.setFrameShape(QFrame.HLine)
        self.hline.setFrameShadow(QFrame.Plain)
        self.hline.setMidLineWidth(0)
        self.hline.setLineWidth(0)
        self.hline.setStyleSheet('border: none; background: {};'.format(AppSettings.SEPARATOR_COLOR))
        self.mainLayout.addWidget(self.hline)

        # Bottom layout
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(0, 0, 0, 0)

        # Results fields
        self.resultsList = QListWidget()
        self.resultsList.setContentsMargins(0, 0, 0, 0)
        self.resultsList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.resultsList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.resultsList.setStyleSheet('border: none; background: {};'.format(AppSettings.BACKGROUND_COLOR))

        self.bottomLayout.addWidget(self.resultsList, 4)

        # TODO Testing stuff, remove after results list appearance is finalized
        for i in range(20):
            item = QListWidgetItem(self.resultsList)
            my_item = FoundItem('Item Item Item %i' % i)
            item.setSizeHint(my_item.sizeHint())
            self.resultsList.addItem(item)
            self.resultsList.setItemWidget(item, my_item)

        self.resultsList.setResizeMode(QListView.Adjust)
        self.resultsList.setSpacing(2)

        # Separator
        self.vline = QFrame()
        self.vline.setFrameShape(QFrame.VLine)
        self.vline.setFrameShadow(QFrame.Plain)
        self.vline.setMidLineWidth(0)
        self.vline.setLineWidth(0)
        self.vline.setStyleSheet('border: none; background:{}'.format(AppSettings.SEPARATOR_COLOR))
        self.bottomLayout.addWidget(self.vline, 0)

        # Details field
        self.detailsField = QLabel('Results go here')
        self.bottomLayout.addWidget(self.detailsField, 6)

        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def search(self, field: str):
        # self.resultsList.clear()
        # for i in range(len(field)):
        #     self.resultsList.addItem(QListWidgetItem('Item %i' % i))

        self.detailsField.setText(field)

    # def focus


class FoundItem(QWidget):
    # confidence allows sorting
    # provider allows to traceback

    def __init__(self, title: str, confidence: int=0, provider: int=0, parent=None):
        super(FoundItem, self).__init__(parent)

        # item layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('background-color: rgb(255,0,255);')

        # TODO elided version of title
        # https://stackoverflow.com/questions/7381100/text-overflow-for-a-qlabel-s-text-rendering-in-qt
        self.titleLabel = QLabel(title)
        self.iconLabel = QLabel()
        self.iconLabel.setPixmap(QPixmap(str(AppSettings.get_resource('', 'logo.png'))).scaledToHeight(30))
        # TODO expose height of result items to settings

        self.mainLayout.addWidget(self.iconLabel, 0)
        self.mainLayout.addWidget(self.titleLabel, 1)

        self.setLayout(self.mainLayout)


class ItemSeparator(QWidget):

    def __init__(self, title: str, parent=None):
        super(ItemSeparator, self).__init__(parent)

        self.title = title


class AppWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        # Frame
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
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

        # Visibility timer for results widget and roll-down/up animations
        # Option A: connect animation finish to visibility, but then there is a perceivable delay
        # Option B: set visibility from the beginning, but then there are weird sizing issues
        # Option C : make a tiny timer that will set visibility on after animation started, but before it's finished
        self.visTimer = QTimer(self)
        self.visTimer.setSingleShot(True)
        self.visTimer.timeout.connect(lambda: self.resultsWidget.setVisible(True))

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

        # Defining roll down animation
        a = QPropertyAnimation(self.parent(), b'minimumHeight')
        a.setDuration(AppSettings.ANIMATION_DURATION)
        a.setStartValue(AppSettings.S_FIELD_HEIGHT)
        a.setEndValue(AppSettings.S_FIELD_HEIGHT + AppSettings.RESULTS_HEIGHT)
        a.setEasingCurve(QEasingCurve.OutBack)
        a.start(QPropertyAnimation.DeleteWhenStopped)

        # Visibility timer
        # Tried different values, but <20 sometimes flickers, >30 sometimes is perceivable
        self.visTimer.start(20)

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

        # Stop visibility timer
        self.visTimer.stop()

        # Need to keep reference, otherwise gets GC'ed immediately
        self.resultsWidget.animation = a

        # Remove border
        # self.searchField.setStyleSheet('border: none;')

    # Assume user stopped typing, start searching
    def do_query(self):
        # TODO more input validation
        query = self.searchField.text()
        if not query:
            return

        # Send data
        self.resultsWidget.search(self.searchField.text())
        print('Searching for', self.searchField.text())

