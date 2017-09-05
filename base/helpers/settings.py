from pathlib import Path
from PyQt5.QtCore import QSettings


class AppSettings(QSettings):
    _singleton = None

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
    def get_resource(name: str) -> Path:
        return AppSettings.instance().resPath / name

