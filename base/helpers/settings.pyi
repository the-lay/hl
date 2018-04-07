from pathlib import Path
from PyQt5.QtGui import QIcon

# QSettings managed entries
WIDTH: int
S_FIELD_HEIGHT: int
RESULTS_HEIGHT: int
ANIMATION_DURATION: int
SEARCH_DELAY: int
PLACEHOLDER_CHANGE_TIME: int
BACKGROUND_COLOR: str
SEPARATOR_COLOR: str

# Runtime generated settings
BASE_PATH: Path
RES_PATH: Path
ICON_PATH: Path
SETTINGS_PATH: Path
PLUGINS_PATH: Path

# Helper functions
def icon_path(a: str) -> str: pass
def icon(a: str) -> QIcon: pass
def log(a) -> None: pass