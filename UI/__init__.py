
from .FilePanel import FilePane
from .ImagePanel import ImagePane
from .OptionsPanel import OptionsPane
from .MainWindow import MainWindow

# This allows us to access our icons by just doing
# QIcon(":<name>") instead of having to specify a full path
# Note that it has to be updated when you add a new icon;
# see assets/assets.qrc and assets/generate.sh
from .qrc_assets import *
from .Config import *
