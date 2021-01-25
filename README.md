# PyQtSA
PyQtSa is a collection of GUI primitives built over PyQt to speed PyQt development
for certain kinds of GUI applications

_NOTE: This README is still in progress as of 10 Jan 2021_

## Overview
This module provides classes that are collections of PyQt objects designed for 
simple and effective presentation in GUI programs. 

Some example objects available through the library include splash screens, 
multi-tab windows, simple buttons, and input forms

### Installation
You will need the PyQt5 library as a prerequisite
```shell script
pip install pyqt5
```
After this, include PyQtSA as a submodule at the same level as your python GUI code
```shell script
git submodule add https://github.com/SpencerArrasmith/PyQtSA path/to/main/python/pyqtsa
git commit -m "Add submodule of PyQtSa repository"
git push
git git submodule update --init --recursive
```

Now add the following lines to the top of your main.py to include the modules 
```python
#!/usr/bin/python

from PyQt5 import QtGui, QtWidgets, QtCore
from pyqtsa.PyQtSA import *
from pyqtsa.widgetStyles import *

# ...
```

From here, you can access the PyQt objects to build your GUI application.

## Example Usage
The example below is the `main()` function of an [FBS-powered](https://build-system.fman.io/) Python 
Qt application that makes use of the PyQtSA `QSATabWidget`.
_**TODO FIXME VERIFY THIS**_
```python
from PyQt5 import QtGui, QtWidgets, QtCore
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys

from pyqtsa.PyQtSA import *
from pyqtsa.widgetStyles import *

from gui_elements.ExampleProtocol import ExampleProtocol

from gui_elements.tabs.TabHome import TabHome
from gui_elements.tabs.TabExample import TabExample
from gui_elements import _version


class ExampleApp(ApplicationContext):
    def __init__(self):
        super().__init__()

        f = open(self.get_resource("style.css"))
        style = f.read()
        f.close()

        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(_version.__appname__)
        self.frame = QtWidgets.QFrame()
        self.window.setCentralWidget(self.frame)

        self.window.setGeometry(0, 0, width=1000, height=500)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.protocol = ExampleProtocol(master=self)

        self.pages = []
        self.pages.append(TabHome(master=self, protocol=self.protocol, index=len(self.pages)))
        self.pages.append(TabExample(master=self, protocol=self.protocol, index=len(self.pages)))

        self.tabs = QSATabWidget(pages=self.pages)

        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.configureTab)
        self.tabs.blockSignals(False)

        self.window.repaint()

        self.tabs.tabBar().setTabButton(self.tabs.index_previous, QTabBar.LeftSide,
                                        self.tabs.pages[self.tabs.index_previous].button_inactive)
        self.tabs.tabBar().setTabButton(self.tabs.currentIndex(), QTabBar.LeftSide,
                                        self.tabs.pages[self.tabs.currentIndex()].button_active)
        self.tabs.index_previous = self.tabs.currentIndex()

        self.layout.addWidget(self.tabs, 2, 0, 1, 10)
        self.frame.setLayout(self.layout)
        self.window.show()

if __name__ == "__main__":
    appctxt = ApplicationContext()
    app = ExampleApp()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
```

## References
* Wiki, API guide, or Doxygen one day
* [PyQt5](https://guiguide.readthedocs.io/en/latest/gui/qt.html)
