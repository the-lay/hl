from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from base.helpers.settings import AppSettings


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

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)

        # Search icon in the field
        painter = QPainter(self)
        icon_pixmap = self.icon.pixmap(QSize(self.iconSize, self.iconSize))
        painter.drawPixmap(8, (self.height() - self.iconSize) // 2, icon_pixmap)
