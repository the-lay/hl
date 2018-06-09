import sys
import types
from pathlib import Path
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtGui import QIcon


class SettingsWrapper(types.ModuleType):

    # For easier auto-complete in IDE, add each new setting to settings.pyi stub
    # TODO: automatic stub file generator

    # List of possible settings. key[0] is the type, key[1] is the default value
    _possible_settings = {
        'WIDTH': (int, 640),
        'S_FIELD_HEIGHT': (int, 40),
        'RESULTS_HEIGHT': (int, 300),
        'ANIMATION_DURATION': (int, 250),
        'SEARCH_DELAY': (int, 150),
        'PLACEHOLDER_CHANGE_TIME': (int, 2000),
        'BACKGROUND_COLOR': (str, '#F6F6F6'),
        'SEPARATOR_COLOR': (str, '#DFDFDF'),
        'SCREEN_NUM': (int, -1),  # -1 means show app on screen where the mouse cursor currently is
        'SOUNDS_ENABLED': (bool, True),
        'ANIMATIONS_ENABLED': (bool, True),
        'GLOBAL_HOTKEY_ENABLED': (bool, True)
    }

    # Generate runtime settings
    # For example paths, which should not be stored in settings ini
    _base_path = Path(__file__).parent.parent.parent
    _res_path = _base_path / 'res'
    _icon_path = _res_path / 'icons'
    _settings_path = _base_path / 'settings.ini'
    _plugins_path = _base_path / 'plugins'
    _runtime_settings = {
        'BASE_PATH': _base_path,
        'RES_PATH': _res_path,
        'ICON_PATH': _icon_path,
        'SETTINGS_PATH': _settings_path,
        'PLUGINS_PATH': _plugins_path
    }

    # TODO: Logging
    @staticmethod
    def log(*whatever):
        print(whatever)

    # Resources
    def icon_path(self, name) -> str:
        return str(self.ICON_PATH / (name + '.png'))

    def icon(self, name) -> QIcon:
        return QIcon(self.icon_path(name))

    # Reset settings to default
    def reset_settings(self):
        for k, v in self._possible_settings.items():
            self._qsettings.setValue(k, v[1])

        self._qsettings.sync()

    # Sync settings
    def sync(self):
        self._qsettings.sync()

    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._runtime = [x for x in dir(self._runtime_settings) if not x.startswith('_')]

        # QSettings setup
        QCoreApplication.setOrganizationName('the-lay')
        QCoreApplication.setOrganizationDomain('gubins.lv')
        QCoreApplication.setApplicationName('Highlight')
        QCoreApplication.setApplicationVersion('0.0.5')

        self._qsettings = QSettings(str(self.SETTINGS_PATH), QSettings.IniFormat)
        self._qsettings.setFallbacksEnabled(False)

        # Check if all possible settings are in ini
        # If not, write new ones
        for key, def_val in self._possible_settings.items():
            if key not in self._qsettings.allKeys():
                print(key, 'is not in qsettings, adding it now')
                self._qsettings.setValue(key, def_val[1])

    # Get/set settings
    def __setitem__(self, key, value):

        if key in self._runtime:
            raise AttributeError('Key ' + key + ' is generated at runtime and is read-only.')

        if key in self._possible_settings:
            return self._qsettings.setValue(key, value)
        else:
            raise AttributeError('Key ' + key + ' is not one of the possible settings.')

    def __getitem__(self, key):
        # if asked for one of the runtime generated settings
        if key in self._runtime_settings:
            return self._runtime_settings[key]

        try:
            return self._qsettings.value(key, type=self._possible_settings[key][0])
        except AttributeError:
            self.log('Can\'t find setting', key)

    # Make it iterable
    def keys(self):
        return list(self._runtime_settings.keys()) + self._qsettings.allKeys()

    # Delegate uppercase attribute requests to getter
    def __getattribute__(self, item: str):

        # if requested attr starts with uppercase, then it is one of the settings
        if item[0].isupper():
            return self[item]

        return super().__getattribute__(item)

sys.modules[__name__] = SettingsWrapper(sys.modules[__name__])
