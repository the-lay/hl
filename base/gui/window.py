from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import random
from typing import List

from ..helpers.settings import *


class SearchField(QLineEdit):
    selectUp = pyqtSignal()
    selectDown = pyqtSignal()
    selectTab = pyqtSignal()

    def placeholder_animation(self) -> None:

        # user is typing something, turn off animation
        if len(str(self.text())) > 0:
            self.placeholderTimer.stop()
            return

        # otherwise start placeholder animation
        self.placeholderTimer.start(0)

    def placeholder_callback(self) -> None:
        # choose random greeting
        new_greeting = random.choice(self.greetings)
        # reroll if it's the same as previous
        while new_greeting == self.currentGreeting:
            new_greeting = random.choice(self.greetings)
        self.currentGreeting = new_greeting

        # set the new placeholder and start timer for next change
        self.setPlaceholderText(new_greeting)
        self.placeholderTimer.start(AppSettings.PLACEHOLDER_CHANGE_TIME)

    def __init__(self):
        super().__init__()

        # Placeholder greetings
        # TODO populate greetings from providers manager
        self.greetings = [
            "wiki 'query'",
            "youtube 'query'",
            "calendar 'query'",
            "imdb 'query'",
            "lyrics 'query'",
            "any file on your PC",
            "help"
        ]
        self.currentGreeting = ''

        # Placeholder timer
        self.placeholderTimer = QTimer(self)
        self.placeholderTimer.timeout.connect(self.placeholder_callback)
        self.textChanged.connect(self.placeholder_animation)
        self.placeholder_animation()

        # Font
        self.fontSize = 14
        f = self.font()
        f.setPointSize(self.fontSize)
        f.setWeight(QFont.Light)
        self.setFont(f)
        f_metric = QFontMetrics(f)

        # Icon
        # TODO when query is processed change icon to something informative? like a green tick
        # TODO and while searching an animated icon?
        self.iconSize = int(f_metric.ascent() * 1.3)
        self.icon = QIcon(str(AppSettings.get_resource('icons', 'search.png')))
        self.setTextMargins(QMargins(self.iconSize + 13, 5, 0, 5))

        # Remove the context menu
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # Border
        self.setStyleSheet('QLineEdit {{ border: none; background-color: {0}; }}'.format(AppSettings.BACKGROUND_COLOR))

        # Intercept all keyboard events
        self.grabKeyboard()

    # Overloading to draw an icon
    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        # TODO: expose in settings whether to draw icon or not
        # Search icon in the field
        painter = QPainter(self)
        icon_pixmap = self.icon.pixmap(QSize(self.iconSize, self.iconSize))
        painter.drawPixmap(8, (self.height() - self.iconSize + 3) // 2, icon_pixmap)

    # Handling down/up button
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Down:
            self.selectDown.emit()
        elif event.key() == Qt.Key_Up:
            self.selectUp.emit()
        elif event.key() == Qt.Key_Tab:
            self.selectTab.emit()
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
        self.setStyleSheet('QWidget {{ border: none; background: {}; }}'.format(AppSettings.BACKGROUND_COLOR))

        # Separator
        self.hline = QFrame()
        self.hline.setFrameShape(QFrame.HLine)
        self.hline.setFrameShadow(QFrame.Plain)
        self.hline.setMidLineWidth(0)
        self.hline.setLineWidth(0)
        self.hline.setStyleSheet('QFrame {{ border: none; background: {}; }}'.format(AppSettings.SEPARATOR_COLOR))
        self.mainLayout.addWidget(self.hline)

        # Bottom layout
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(0, 0, 0, 0)

        # Results fields
        self.resultsList = QListWidget()
        self.resultsList.setFocusPolicy(Qt.NoFocus)
        self.resultsList.setContentsMargins(0, 0, 0, 0)
        self.resultsList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.resultsList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.resultsList.setStyleSheet('QListWidget {{ border: none; background: {}; }}'
                                       .format(AppSettings.BACKGROUND_COLOR))
        self.resultsList.setUniformItemSizes(True)
        # self.resultsList.setStyleSheet('QListWidget::item { border-bottom: 1px solid black; }')
        self.resultsList.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.MinimumExpanding)

        self.bottomLayout.addWidget(self.resultsList, 4)  # TODO expose results list to details ratio

        self.resultsList.setResizeMode(QListView.Adjust)
        self.resultsList.setSpacing(0)

        # Separator
        self.vline = QFrame()
        self.vline.setFrameShape(QFrame.VLine)
        self.vline.setFrameShadow(QFrame.Plain)
        self.vline.setMidLineWidth(0)
        self.vline.setLineWidth(0)
        self.vline.setStyleSheet('QFrame {{ border: none; background:{}; }}'.format(AppSettings.SEPARATOR_COLOR))
        self.bottomLayout.addWidget(self.vline, 0)

        # Details field
        self.resultDetails = QLabel()
        self.resultDetails.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.MinimumExpanding)
        self.bottomLayout.addWidget(self.resultDetails, 6)  # TODO expose results list to details ratio

        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

        self.setFocusPolicy(Qt.NoFocus)

        # Provider manager results connections
        AppSettings.get_provider_manager().resultsFound.connect(self.receive_results)

    def receive_results(self, results: List) -> None:

        for i in range(len(results)):
            item = QListWidgetItem(self.resultsList)
            my_item = FoundItem('{}'.format(results[i]), confidence=(int(i) * 10))
            item.setSizeHint(my_item.sizeHint())
            self.resultsList.addItem(item)
            self.resultsList.setItemWidget(item, my_item)

        # TODO sort items by confidence

        # Select the first row
        self.resultsList.setCurrentRow(0)

        # placeholder, TODO remove when resultDetails widget implemented
        self.resultDetails.setText(', '.join(results))


class FoundItem(QWidget):
    # confidence allows sorting
    # provider allows to traceback

    def __init__(self, title: str, icon: str='logo', confidence: int=0, provider: int=0, parent=None):
        super(FoundItem, self).__init__(parent)

        # item layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # same left-margin as search lens in the main bar
        self.mainLayout.setSpacing(0)
        self.setStyleSheet('background: {};'.format(AppSettings.BACKGROUND_COLOR))

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setSpacing(7)

        # TODO elided version of title
        # https://stackoverflow.com/questions/7381100/text-overflow-for-a-qlabel-s-text-rendering-in-qt

        self.iconLabel = QLabel()
        self.iconLabel.setContentsMargins(8, 0, 0, 0)
        self.iconLabel.setPixmap(QPixmap(str(AppSettings.get_resource('', icon + '.png'))).scaledToHeight(30))
        # TODO expose height of result items to settings

        self.detailsLayout = QVBoxLayout()
        self.detailsLayout.setContentsMargins(0, 0, 0, 0)
        self.detailsLayout.setSpacing(0)

        self.titleLabel = QLabel(title)
        self.detailsLayout.addWidget(self.titleLabel)
        self.confidenceLabel = QLabel(str(confidence))
        self.detailsLayout.addWidget(self.confidenceLabel)

        self.bottomLayout.addWidget(self.iconLabel, 0)
        self.bottomLayout.addLayout(self.detailsLayout, 1)
        self.mainLayout.addLayout(self.bottomLayout)

        # divider
        self.hline = QFrame()
        self.hline.setFrameShape(QFrame.HLine)
        self.hline.setFrameShadow(QFrame.Plain)
        self.hline.setMidLineWidth(0)
        self.hline.setLineWidth(0)
        self.hline.setStyleSheet('border: none; background: {};'.format(AppSettings.SEPARATOR_COLOR))
        self.mainLayout.addWidget(self.hline)

        self.setLayout(self.mainLayout)


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
        self.searchField.selectUp.connect(lambda: self.select_up())
        self.searchField.selectDown.connect(lambda: self.select_down())
        self.searchField.selectTab.connect(lambda: self.select_tab())

    # Triggered upon change in search field
    # Handles results widget toggling and delaying search query
    def text_input(self, field: str) -> None:

        # Results widget opening/closing
        if not field:
            self.roll_up()

            # Reset flag
            self.resultsOpen = False

            # Stop executing further
            return

        # Ignore if last character is a blank space
        # TODO: good idea, but needs more thought
        # for example: ctrl+backspace remove the last word, but leaves the space
        # elif field.endswith(' '):
        #     return

        # Add a delay on search
        self.searchTimer.start(AppSettings.SEARCH_DELAY)

    # TODO behavior of up/down/tab should be defined through settings
    def select_down(self) -> None:
        # TODO what way up/down goes
        current_row = self.resultsWidget.resultsList.currentRow() + 1

        # TODO does it scroll through or stops on the top/bottom row
        max_row = self.resultsWidget.resultsList.count() - 1
        if current_row > max_row:
            current_row = max_row

        self.resultsWidget.resultsList.setCurrentRow(current_row)

    # TODO same as select_down
    def select_up(self) -> None:
        current_row = self.resultsWidget.resultsList.currentRow() - 1

        if current_row < 0:
            current_row = 0

        self.resultsWidget.resultsList.setCurrentRow(current_row)

    # TODO same as select_down
    def select_tab(self) -> None:
        current_row = self.resultsWidget.resultsList.currentRow() + 1

        max_row = self.resultsWidget.resultsList.count() - 1
        if current_row > max_row:
            current_row = 0

        self.resultsWidget.resultsList.setCurrentRow(current_row)

    # Roll window down
    def roll_down(self) -> None:
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
        self.visTimer.start(25)

        # Need to keep reference, otherwise gets GC'ed immediately
        self.resultsWidget.animation = a

    # Roll window up
    def roll_up(self) -> None:
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

        # Clear results
        self.clear_results()

    # Clear results list and result details
    def clear_results(self) -> None:
        self.resultsWidget.resultsList.clear()
        self.resultsWidget.resultDetails.clear()

    # Assume user stopped typing, start searching
    # If the widget is not open, roll down the window
    def do_query(self) -> None:
        # TODO more input validation
        query = self.searchField.text()
        if not query:
            return

        # If results widget is not seen, open it
        if not self.resultsOpen:
            # Roll the window
            self.roll_down()

            # Set flag
            self.resultsOpen = True

        # Clear previous results
        self.clear_results()

        # Pass input field to provider manager
        # manager does fuzz search for providers

        # TODO color recognized keywords?
        # https://stackoverflow.com/questions/14417333/how-can-i-change-color-of-part-of-the-text-in-qlineedit

        AppSettings.get_provider_manager().search(query)
        print('Searching for', query)

