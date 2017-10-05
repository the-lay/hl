from pathlib import Path
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon


class AppSettings(QSettings):
    _singleton = None
    WIDTH = 640
    S_FIELD_HEIGHT = 40
    RESULTS_HEIGHT = 300
    ANIMATION_DURATION = 350

    @staticmethod
    def instance():
        if not AppSettings._singleton:
            AppSettings._singleton = AppSettings()

        return AppSettings._singleton

    def __init__(self):
        # Calculating paths
        self.basePath = Path(__file__).parent.parent.parent
        self.resPath = self.basePath / 'res'
        self.settingsPath = self.basePath / 'settings.ini'

        # Init
        QSettings.__init__(self, str(self.settingsPath), QSettings.IniFormat)
        self.setFallbacksEnabled(False)

    @staticmethod
    def get_resource(category: str, name: str) -> Path:
        return AppSettings.instance().resPath / category / name
    #
    # @staticmethod
    # def get_icon(name: str) -> QIcon:
    #     path = AppSettings.instance().resPath / 'icons' / name
    #     return QIcon(str(path))
