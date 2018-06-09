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
SCREEN_NUM: int
SOUNDS_ENABLED: bool
ANIMATIONS_ENABLED: bool
GLOBAL_HOTKEY_ENABLED: bool

# Runtime generated settings
BASE_PATH: Path
RES_PATH: Path
ICON_PATH: Path
SETTINGS_PATH: Path
PLUGINS_PATH: Path

# Overloaded
def __getitem__(key): pass
def __setitem__(key, value): pass

# Helper functions
def icon_path(a: str) -> str: pass
def icon(a: str) -> QIcon: pass
def log(a) -> None: pass
def sync() -> None: pass
def keys() -> list(str): pass