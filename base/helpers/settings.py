import sys
from pathlib import Path
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtGui import QIcon


# Resources
def icon_path(name) -> str:
    return str(iconPath / (name + '.png'))


def icon(name) -> QIcon:
    return QIcon(icon_path(name))


# Available settings with type and default value
default_values = {
    'WIDTH': (int, 640),
    'S_FIELD_HEIGHT': (int, 40),
    'RESULTS_HEIGHT': (int, 300),
    'ANIMATION_DURATION': (int, 250),
    'SEARCH_DELAY': (int, 150),
    'PLACEHOLDER_CHANGE_TIME': (int, 2000),
    'BACKGROUND_COLOR': (str, 'rgb(246,246,246)'),
    'SEPARATOR_COLOR': (str, 'rgb(223,223,223)')
}

# This block is here only for IDE, the values are overwritten later anyway (setattr(...))
# TODO maybe remove this later on?
# TODO is there a better way to do all this?
WIDTH = 640
S_FIELD_HEIGHT = 40
RESULTS_HEIGHT = 300
ANIMATION_DURATION = 250
SEARCH_DELAY = 150
PLACEHOLDER_CHANGE_TIME = 500
BACKGROUND_COLOR = 'rgb(246,246,246)'
SEPARATOR_COLOR = 'rgb(223,223,223)'

# Paths
# TODO is there a better way to specify base path?
basePath = Path(__file__).parent.parent.parent
resPath = basePath / 'res'
iconPath = resPath / 'icons'
settingsPath = basePath / 'settings.ini'
pluginsPath = basePath / 'plugins'

# QSettings setup
QCoreApplication.setOrganizationName('the-lay')
QCoreApplication.setOrganizationDomain('gubins.lv')
QCoreApplication.setApplicationName('Highlight')
QCoreApplication.setApplicationVersion('0.0.3')

qsettings = QSettings(str(settingsPath), QSettings.IniFormat)
qsettings.setFallbacksEnabled(False)

# Set default values if settings.ini does not exist or only partial values
for setting, value in default_values.items():
    if not qsettings.value(setting):
        qsettings.setValue(setting, value[1])
        print('setting qsettings value for ', setting)

# Populate module attributes - syntactic sugar pretty much
for key in qsettings.allKeys():
    setattr(sys.modules[__name__], key, qsettings.value(key, type=default_values[key][0]))

# TODO Leaving previous approaches for later, might revert back / try them again later


# class Settings(ModuleType):
#
#     def __getattr__(self, item):
#         print('getting', item)
#         return getattr(self, item)
#
#     # def __setattr__(self, k, v):
#     #     print('setting', k, v)
#     #     setattr(sys.modules[__name__], k, qsettings.value(v, type=default_values[k][0]))
#
#
# sys.modules[__name__] = Settings(__name__)

#
#
# class AppSettings(dict):
#
#     # Singleton
#     __instance = None
#
#     def __new__(cls):
#         if not AppSettings.__instance:
#             AppSettings.__instance = AppSettings.__Impl()
#
#         return AppSettings.__instance
#
#     def __getattr__(self, item):
#         return getattr(self.__instance, item)
#
#     def __setattr__(self, key, value):
#         return setattr(self.__instance, key, value)
#
#     # Actual settings implementation
#     class __Impl:
#
#         def __init__(self):
#             # Paths
#             self.basePath = Path(__file__).parent.parent.parent
#             self.resPath = self.basePath / 'res'
#             self.iconPath = self.resPath / 'icons'
#             self.settingsPath = self.basePath / 'settings.ini'
#
#             # QSettings setup
#             QCoreApplication.setOrganizationName('the-lay')
#             QCoreApplication.setOrganizationDomain('gubins.lv')
#             QCoreApplication.setApplicationName('Highlight')
#             QCoreApplication.setApplicationVersion('0.0.2')
#
#             self.qsettings = QSettings(str(self.settingsPath), QSettings.IniFormat)
#             self.qsettings.setFallbacksEnabled(False)
#
#             # Set default values
#             self.reset_settings()
#
#         # Reset settings - default values
#         def reset_settings(self):
#             # TODO expose all these values in a settings window
#             default_settings = {
#                 'WIDTH': 640,
#                 'S_FIELD_HEIGHT': 40,
#                 'RESULTS_HEIGHT': 300,
#                 'ANIMATION_DURATION': 250,
#                 'SEARCH_DELAY': 150,
#                 'PLACEHOLDER_CHANGE_TIME': 2000,
#                 'BACKGROUND_COLOR': 'rgb(246,246,246)',
#                 'SEPARATOR_COLOR': 'rgb(223,223,223)'
#             }
#
#             for setting, value in default_settings.items():
#                 if not self.qsettings.value(setting):
#                     self.qsettings.setValue(setting, value)
#
#         # Resources
#         def icon(self, name):
#             return self.iconPath / (name + '.png')
#
#         # Returns all set settings, mostly for debugging
#         @property
#         def set_settings(self):
#             return self.keys()
#
#         # Allow access to settings in a cool dict-like fashion
#         def __iter__(self):
#             return (key for key in self.qsettings.allKeys())
#
#         def __setitem__(self, key, value):
#             self.qsettings.setValue(key, value)
#
#         def __getitem__(self, key):
#             return self.qsettings.value(key)
#
#         def keys(self):
#             return [key for key in self.qsettings.allKeys()]
#
#         def values(self):
#             return [self.qsettings.value(key) for key in self.qsettings.allKeys()]
#
#         def itervalues(self):
#             return (self.qsettings.value(key) for key in self.qsettings.allKeys())
