from .SubscriberVariable import SubscriberVariable
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QEvent, QObject
from PyQt5.QtGui import QPixmap, QColor, QBitmap, QPalette, QBrush

from .widgetStyles import *

import time


class QSANullEffect(QGraphicsEffect):
    """A null graphics effect for clearing other effects"""
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setEnabled(False)


class QSADropShadow(QGraphicsDropShadowEffect):
    """A subtle drop shadow for buttons"""
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setBlurRadius(5)
        self.setColor(QColor(0, 0, 0, 250))
        self.setXOffset(0)
        self.setYOffset(0)


class QSABaseFrame(QFrame):
    """A rectangular GUI region for a specific purpose"""
    def __init__(self, master=None,
                 row=0, column=0):

        super().__init__()

        self.master = master
        self.row = row
        self.column = column

        self.setFixedWidth(220)
        self.setFixedHeight(50)

        self.setStyleSheet(widgetStyle_QSABaseFrame)

    def getReadCommand(self):
        """Build the command to send when reading a parameter"""
        return ""

    def getWriteCommand(self):
        """Build the command to send when writing a parameter"""
        return ""


class QSASplash(QSplashScreen):
    """A splash screen which displays a series of messages at the bottom"""
    def __init__(self, master=None, image=None, mask=None):
        self.master = master
        self.imagefile = image
        self.image = QPixmap(self.imagefile)
        super().__init__(self.image, Qt.WindowStaysOnTopHint)

        self.setStyleSheet(widgetStyle_splash)

        self.maskfile = mask
        self.mask = QBitmap(self.maskfile)
        self.setMask(self.mask)

        self.messages = []
        self.delays = []
        self.AddMessage("Loading", 0.2)
        self.messageIndex = 0

        self.show()

        self.showMessage(self.messages[self.messageIndex], Qt.AlignCenter | Qt.AlignBottom)
        time.sleep(self.delays[self.messageIndex])

    def AddMessage(self, message="", delay=0):
        self.messages.append(message)
        self.delays.append(delay)

    def NextMessage(self, timed=True):
        self.messageIndex += 1
        if len(self.messages) == self.messageIndex + 1:
            self.finish(self.master)
            self.messageIndex = 0
        else:
            self.showMessage(self.messages[self.messageIndex], Qt.AlignCenter | Qt.AlignBottom)
            if timed:
                time.sleep(self.delays[self.messageIndex])

    def Finish(self):
        self.finish(self.master)


class QSAPopup(QDialog):
    """A base popup window object"""
    def __init__(self, master=None, title=""):
        super().__init__()
        self.master = master
        self.title = title
        self.setWindowTitle(self.title)
        self.setStyleSheet(widgetStyle_popup)

        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        self.setLayout(self.layout)


class QSATextPopup(QSAPopup):
    """A popup window to display a text block"""
    def __init__(self, master=None, title="", text=""):
        super().__init__(master=master, title=title)
        self.text = text
        self.label = QLabel()
        self.label.setText(self.text)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setStyleSheet(widgetStyle_popup)
        self.layout.addWidget(self.label)


class QSALoginPopup(QSAPopup):
    """A popup window to trigger a callback when the correct username and password are provided"""
    def __init__(self, master=None, callback=None):
        super().__init__(master=master)

        self.callback = callback

    # The username and password
        self.username = "spencer"
        self.password = "arrasmith"

        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        self.label_logo = QLabel()
        self.pixmap_logo = QPixmap(self.master.get_resource('images/adminmode_300.png'))
        self.label_logo.setPixmap(self.pixmap_logo)

        self.label_user = QLabel("User Name")
        self.label_user.setAttribute(Qt.WA_TranslucentBackground)
        self.field_user = QLineEdit()
        self.label_pass = QLabel("Password")
        self.label_pass.setAttribute(Qt.WA_TranslucentBackground)
        self.field_pass = QLineEdit()
        self.field_pass.setEchoMode(QLineEdit.Password)
        self.button_login = QPushButton("Log In")
        self.button_login.clicked.connect(self.login)

        self.layout.addWidget(self.label_logo, 0, 0, 1, 2)
        self.layout.addWidget(self.label_user, 1, 0)
        self.layout.addWidget(self.field_user, 1, 1)
        self.layout.addWidget(self.label_pass, 2, 0)
        self.layout.addWidget(self.field_pass, 2, 1)
        self.layout.addWidget(self.button_login, 3, 0, 1, 2)

        self.setFixedSize(330, 180)
        self.field_user.setFocus()

    def login(self):
        """Trigger the callback when the correct username and password are provided"""
        if self.field_user.text() == self.username and self.field_pass.text() == self.password:
            self.callback(True)
            self.close()
        else:
            self.field_pass.setText("")
            self.field_pass.setFocus()


class QSALogoutPopup(QSAPopup):
    """A popup window to trigger a callback when the button is pressed"""
    def __init__(self, master=None, callback=None):
        super().__init__()

        self.callback = callback

        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        self.label_logo = QLabel()
        self.pixmap_logo = QPixmap(self.master.get_resource('images/adminmode_300.png'))
        self.label_logo.setPixmap(self.pixmap_logo)

        self.button_logout = QPushButton("Log Out")
        self.button_logout.clicked.connect(self.logout)

        self.layout.addWidget(self.label_logo, 0, 0, 1, 2)
        self.layout.addWidget(self.button_logout, 3, 0, 1, 2)

        self.setLayout(self.layout)
        self.setFixedSize(330, 180)

    def logout(self):
        """Trigger the callback"""
        self.callback(False)
        self.close()


class QSATab(QFrame):
    """A GUI region which contains all parameters relevant to one subsystem"""
    def __init__(self, master=None, serial=None, protocol=None, title="", icon="", index=0, widgets=[], widthActive=160, widthInactive=80):
        super().__init__()

        self.master = master
        self.serial = serial
        self.protocol = protocol

        self.setContextMenuPolicy(Qt.PreventContextMenu)
        #self.setAutoFillBackground(False)

        self.title = title
        self.label_title = QLabel(title)
        self.label_title.setAttribute(Qt.WA_TranslucentBackground)

        self.index = index
        self.widthActive = widthActive
        self.widthInactive = widthInactive

    # A simple visual representation of the subsystem
        self.iconfile = self.master.get_resource(icon)
        self.icon = QLabel()
        self.icon.setAttribute(Qt.WA_TranslucentBackground)
        if len(self.iconfile):
            self.iconpix = QPixmap(self.iconfile)
            self.icon.setPixmap(self.iconpix)

    # Build the look of the tab for when it is active
        self.button_active = QGroupBox()
        self.button_active.setFixedHeight(46)
        self.button_active.setFixedWidth(self.widthActive)
        self.layout_buttonactive = QGridLayout()
        #self.layout_buttonactive.addWidget(self.icon, 0, 0)
        self.layout_buttonactive.addWidget(self.label_title, 0, 0)
        self.button_active.setLayout(self.layout_buttonactive)
        self.button_active.setStyleSheet(widgetStyle_tabActive)
        #self.button_active.setAttribute(Qt.WA_TranslucentBackground)
        self.button_active.setContextMenuPolicy(Qt.CustomContextMenu)
        self.button_active.customContextMenuRequested.connect(self.contextMenuEvent)

    # Build the look of the tab for when it is inactive
        self.button_inactive = QGroupBox()
        self.button_inactive.setFixedHeight(46)
        self.button_inactive.setFixedWidth(self.widthInactive)
        self.layout_buttoninactive = QGridLayout()
        self.button_inactive.setLayout(self.layout_buttoninactive)
        self.layout_buttoninactive.addWidget(self.icon, 0, 0)
        #self.layout_buttonactive.addWidget(QLabel(title), 0, 1)
        self.button_inactive.setStyleSheet(widgetStyle_tabInactive)
        self.button_inactive.setAttribute(Qt.WA_TranslucentBackground)
        self.button_inactive.setToolTip(self.title)

    # Add widgets to the tab window
        self.widgets = widgets

        self.layout = QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(10,10,10,10)
        self.setStyleSheet(widgetStyle_QSATab)

        row = 0
        for widget in self.widgets:
            self.layout.addWidget(widget, row, 0, 1, 5)
            try:
                widget.setAlignment(Qt.AlignRight | Qt.AlignTop)
            except:
                continue
            row += 1

    # Fill the bottom with a variable-size widget to keep all others pushed against the top of the region
        self.filler = QWidget()
        self.filler.setSizePolicy(QSizePolicy.Expanding | QSizePolicy.Preferred, QSizePolicy.Expanding | QSizePolicy.Preferred)
        self.filler.setAttribute(Qt.WA_TranslucentBackground)
        self.filler.setContextMenuPolicy(Qt.PreventContextMenu)
        self.layout.addWidget(self.filler, row, 0, 1, 5)

        self.setLayout(self.layout)

    def contextMenuEvent(self, event):
        contextMenu = QMenu()

        action3 = QAction(text="Save to File")
        action3.triggered.connect(self.SaveToFile)
        contextMenu.addAction(action3)

        action4 = QAction(text="Load from File")
        action4.triggered.connect(self.LoadFromFile)
        contextMenu.addAction(action4)

        event.setX(event.x() + self.index * 86)
        event.setY(event.y() - 40)
        contextMenu.exec_(self.mapToGlobal(event))

    def ListAllWidgets(self):
        """Prepare a flat list of all widgets and subwidgets on the tab"""
        widgetlist = []
        for widget in self.widgets:
            if widget.widget:
                if isinstance(widget, QSAWidgetCluster):
                    if len(widget.widgets) > 1:
                        for frame in widget.widgets:
                            widgetlist.append(frame)
                            if isinstance(frame, QSAVariableFrame):
                                for constant in frame.constants:
                                    widgetlist.append(constant)
                elif isinstance(widget, QSAParameterCluster):
                    if widget.widget:
                        widgetlist.append(widget.widget)
                        if isinstance(widget.widget, QSAVariableFrame):
                            for constant in widget.widget.constants:
                                widgetlist.append(constant)
        return widgetlist

    def SaveToFile(self):
        """Save all parameter names and values to a csv file"""
        filename = "".join(self.title.split(" "))
        filename = "".join(filename.split(".")) + "_Presets.csv"
        try:
            f = open(filename, 'w+')
        except :
            return

        presets = ""
        savequeue = self.ListAllWidgets()
        for widget in savequeue:
            if isinstance(widget, QSAVariableFrame):
                if widget.parameter:
                    if 'W' in widget.parameter.permission:
                        presets += widget.parameter.parameter + ',' + str(widget.parameter.variable.value) + '\n'

        f.write(presets)
        f.close()

    def LoadFromFile(self):
        """Load all parameter values from a csv file"""
        filename = "".join(self.title.split(" "))
        filename = "".join(filename.split(".")) + "_Presets.csv"
        try:
            f = open(filename, 'r')
        except:
            return

        loadedvalues = f.read()
        f.close()
        loadedarray = [x.split(',') for x in loadedvalues.split('\n')]

        for line in loadedarray:
            if line[0] in self.protocol.parameters.keys():
                if 'W' in self.protocol.parameters[line[0]].permission:
                    if 'P' not in self.protocol.parameters[line[0]].permission or self.master.inAdminMode:
                        try:
                            float(line[1])
                            self.protocol.parameters[line[0]].variable.value = float(line[1])
                        except ValueError:
                            self.protocol.parameters[line[0]].variable.value = line[1]
                        except:
                            continue

    def SlowAllTimers(self, slow):
        for widget in self.ListAllWidgets():
            if isinstance(widget, QSAReadout) or isinstance(widget, QSAMathFrame):
                if slow:
                    widget.interval = 60
                else:
                    widget.interval = widget.defaultinterval


class QSATabWidget(QTabWidget):
    """A container object for adding tabs to"""
    def __init__(self, pages=None):
        super().__init__()
        self.setStyleSheet(widgetStyle_tabBar)

        self.pages = pages
        self.index_previous = 0
        for i, page in enumerate(pages):
            self.addTab(page, "")#, page.title)
            if page.icon:
                #self.setTabIcon(i, page.icon)
                self.tabBar().setTabButton(i, QTabBar.LeftSide, page.button_inactive)

    def previousIndex(self):
        return self.index_previous


class QSAParameterCluster(QGroupBox):
    """A horizontal box which contains a label on the left and a widget on the right"""
    def __init__(self, master=None, serial=None,
                 text="", widget="",
                 row=0, column=0):

        super().__init__()

        self.master = master
        self.serial = serial

        self.text = text
        self.widget = widget

        self.row = row
        self.column = column

        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 1, 5, 1)

        self.setContextMenuPolicy(Qt.PreventContextMenu)
        #self.setAutoFillBackground(False)
        self.setStyleSheet(widgetStyle_QSAParameterCluster)

        self.label_group = QLabel()
        self.label_group.setText(self.text)
        #self.label_group.setStyleSheet(widgetStyle_QSAParameterCluster)

        self.layout.addWidget(self.label_group, 0, 0, 1, 1)
        self.label_group.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if self.widget:
            self.layout.addWidget(self.widget, 0, 1, 1, 1)

        self.setLayout(self.layout)
        self.setFixedHeight(60)


    def setAdminMode(self, adminmode : bool):
        """Hide this widget if admin mode is not enabled and the parameter is protected"""
        if not adminmode:
            if self.widget:
                if self.widget.parameter:
                    if "P" in self.widget.parameter.permission:
                        self.hide()
                    else:
                        self.show()
            else:
                self.show()
        else:
            self.show()


class QSAWidgetCluster(QSAParameterCluster):
    """A parameter cluster which may contain multiple widgets"""
    def __init__(self, master=None, serial=None,
                 text="", widgets=[],
                 row=0, column=0):

        if not len(widgets) > 0:
            widgets = [None]
        super().__init__(master=master, serial=serial, text=text, widget=widgets[0], row=row, column=column)

        self.layout.removeWidget(self.widget)
        self.widgets = widgets

        col = 2
        if len(widgets) > 0:
            for widget in widgets:
                self.layout.addWidget(widget, 0, col)
                #widget.setAlignment(Qt.AlignRight | Qt.AlignTop)
                col += 1


class QSAConstantsPopup(QSAPopup):
    """A popup window for editing a list of constants related to a single parameter"""
    def __init__(self, master=None, serial=None,
                 text="",
                 constants=[],
                 row=0, column=0):

        super().__init__(master=master, title="")

        self.serial = serial

        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.StrongFocus)

        self._constants = constants

        self.row = row
        self.column = column

        self.layout.setContentsMargins(1, 1, 1, 1)
        self.setFixedWidth(304)

        self.isPopulated = False
        self.populate()


    # Text - the header of this cluster
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.setWindowTitle(self._text)

    @text.getter
    def text(self):
        return self._text

    # Constants - a list of the constants variables in the cluster
    @property
    def constants(self):
        return self._constants

    @constants.setter
    def constants(self, constants):
        self._constants = constants
        self.populate()

    @constants.getter
    def constants(self):
        return self._constants


    def populate(self):
        """Fill in the window with the provided list of widgets"""
        row = 0
        if self._constants:
            if len(self._constants):
                for widget in self._constants:
                    try:
                        self.layout.addWidget(widget, row, 0)
                        row += 1
                    except:
                        return
                #self.setFixedHeight(len(self._constants) * 55)
            else:
                self.hide()


class QSAVariableFrame(QSABaseFrame):
    """A small region which has information tied to a serial parameter"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 text="",
                 constants=[]
                 ):

        super().__init__(master=master, row=row, column=column)

        self.parameter = parameter
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 1, 5, 1)

        self.constants = constants


        if len(self.constants):
            self.button_expand = QSAPlusButton()
            self.layout.addWidget(self.button_expand, 0, 6)
            self.button_expand.clicked.connect(self.expandConstants)
            self.constantsPopup = QSAConstantsPopup(master=self, constants=self.constants)

        if text:
            self._text = text
        else:
            self._text = self.parameter.parameter
        self.label = QLabel()
        self.label.setText(self.text)

        self.layout.addWidget(self.label, 0, 0)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        if parameter:
            self.description = self.parameter.description
            self.command = self.parameter.command
        else:
            self.description = ""
            self.command = ""
        self.index = index

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        self.label.setText(t)

    def getReadCommand(self):
        """Build the command to send when reading a parameter"""
        if self.command:
            return self.command + 'R'
        else:
            return ""

    def getWriteCommand(self):
        """Build the command to send when writing a parameter"""
        if self.command:
            return self.command + 'W'
        else:
            return ""

    def expandConstants(self):
        """Show a popup window to adjust a parameter's constants"""
        count = 0
        for constant in self.constantsPopup.constants:
            if "P" not in constant.parameter.permission or self.master.master.master.inAdminMode:
                constant.show()
                count += 1
            else:
                constant.hide()
        if count > 0:
            self.constantsPopup.show()
            self.constantsPopup.setFixedHeight(count * 55)
            self.constantsPopup.setWindowTitle(self.master.text + " " + self.text[:-1] + " - Constants")


class QSAEntry(QSAVariableFrame):
    """A small region containing an editable field, units label, and button for constants popup"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 text="",
                 constants=[]
                 ):

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, text=text, constants=constants)

        self.master = master

        self.units = self.parameter.units
        self.precision = self.parameter.precision
        self.mode = self.parameter.mode
        self.value_min = self.parameter.value_min
        self.value_max = self.parameter.value_max

        self.row = row
        self.column = column

        self.index = index
        self.command = self.parameter.command

        self.spinbox_set = QDoubleSpinBox()
        #self.spinbox_set.setFixedWidth(80)
        self.parameter.variable.bind_to(self.updateValue)
        self.spinbox_set.setButtonSymbols(2)
        self.spinbox_set.setMinimum(self.value_min)
        self.spinbox_set.setMaximum(self.value_max)
        self.spinbox_set.setDecimals(self.precision)
        self.spinbox_set.setSingleStep(10**-self.precision)     # Step size is the smallest visible decimal digit
        self.spinbox_set.setContextMenuPolicy(Qt.PreventContextMenu)
        self.label_units = QLabel()
        self.label_units.setText(self.units)

        self.spinbox_set.setStyleSheet(widgetStyle_spinboxSet)

        self.layout.addWidget(self.spinbox_set, 0, 1, 1, 4)
        self.spinbox_set.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.spinbox_set.setFixedWidth(90)
        self.layout.addWidget(self.label_units, 0, 5)
        self.label_units.setFixedWidth(40)
        self.label_units.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def setReadOnly(self, value):
        """Lock editing of the field"""
        self.spinbox_set.setReadOnly(value)

    def updateValue(self, value=None):
        """Update the displayed value when the serial parameter variable changes"""
        self.spinbox_set.setValue(self.parameter.variable.value)

    def updateParameter(self, value=None):
        """Update the serial parameter variable when the displayed value changes"""
        self.parameter.variable.value = self.spinbox_set.value()

    def updateMinimum(self, value):
        """Update the minimum value of the spinbox - bind this to a constant entry to synchronize it"""
        self.spinbox_set.setMinimum(value)

    def updateMaximum(self, value):
        """Update the maximum value of the spinbox - bind this to a constant entry to synchronize it"""
        self.spinbox_set.setMaximum(value)

    def getWriteCommand(self):
        """Build the command to send when writing a parameter"""
        self.parameter.variable.value = self.spinbox_set.value()
        var = str(self.parameter.variable.value)
        if len(var) > 8:
            var = var[:8]
        return self.command + 'W' + var


class QSAConstantEntry(QSAEntry):
    """A small region containing an editable field and a units label for constants"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 text="",
                 instant=False
                 ):
        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, text=text)
        self.setFixedWidth(300)
        self.label.setFixedWidth(120)
        self.spinbox_set.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.spinbox_set.setFixedWidth(120)
        self.updateValue()
        self.label_units.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.isInstant = instant

        if self.isInstant:
            self.spinbox_set.valueChanged.connect(self.updateParameter)


class QSAReadout(QSAVariableFrame):
    """A small region containing a non-editable readout field and a units label which polls a parameter"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 text="", interval=0,
                 constants=[]
                 ):

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, text=text, constants=constants)

        self.units = self.parameter.units
        self.precision = self.parameter.precision
        self.mode = self.parameter.mode

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll)
        self.interval = interval
        self.defaultinterval = interval

        self.spinbox_read = QDoubleSpinBox()
        self.spinbox_read.setMinimum(-float("inf"))
        self.spinbox_read.setMaximum(float("inf"))
        self.parameter.variable.bind_to(self.updateValue)
        self.spinbox_read.setButtonSymbols(2)
        self.spinbox_read.setReadOnly(True)
        self.spinbox_read.setDecimals(self.precision)
        self.spinbox_read.setToolTip(self.description)
        self.spinbox_read.setContextMenuPolicy(Qt.PreventContextMenu)
        self.label_units = QLabel()
        self.label_units.setText(self.units)
        self.label_units.setFixedWidth(40)

        self.label.setStyleSheet(widgetStyle_textActual)
        self.spinbox_read.setStyleSheet(widgetStyle_spinboxActual)
        self.label_units.setStyleSheet(widgetStyle_textActual)

        self.layout.addWidget(self.spinbox_read, 0, 1, 1, 3)
        self.spinbox_read.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.layout.addWidget(self.label_units, 0, 4)
        self.label_units.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        if interval >= 100:
            self._interval = abs(interval / 1000)
        else:
            self._interval = abs(interval)
        if self._interval > 0:
            self.timer.setInterval(self._interval * 1000)
            self.timer.start()
        else:
            self.timer.setSingleShot(True)

    @interval.getter
    def interval(self):
        return self._interval

    def poll(self):
        """Read the parameter at a regular interval"""
        if len(self.parameter.command):
            self.master.serial.sendSerial(message = self.getReadCommand())

    def updateValue(self, value):
        """Update the displayed value when the serial parameter variable changes"""
        self.spinbox_read.setValue(self.parameter.variable.value)


class QSAInfoFrame(QSAVariableFrame):
    """A small region to display informational text"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 text="",
                 interval=0,
                 constants=[]):

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, text=text, constants=constants)

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll)
        self.interval = interval
        self.defaultinterval = interval

        self.label.setFixedWidth(100)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label_info = QLabel()
        self.label_info.setFixedWidth(150)
        self.label_info.setAttribute(Qt.WA_TranslucentBackground)
        self.parameter.variable.bind_to(self.updateValue)
        self.label_info.setToolTip(self.description)

        self.label.setStyleSheet(widgetStyle_textActual)
        self.label_info.setStyleSheet(widgetStyle_textActual)

        self.layout.addWidget(self.label_info, 0, 1, 1, 3)
        self.label_info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.updateValue()

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        if interval >= 100:
            self._interval = abs(interval / 1000)
        else:
            self._interval = abs(interval)
        if self._interval > 0:
            self.timer.setInterval(self._interval * 1000)
            self.timer.start()
        else:
            self.timer.setSingleShot(True)

    @interval.getter
    def interval(self):
        return self._interval

    def poll(self):
        """Read the parameter at a regular interval"""
        self.updateValue()

    def updateValue(self, text=None):
        """Update the displayed value when the serial parameter variable changes"""
        if text:
            self.label_info.setText(str(text))
        else:
            self.label_info.setText(str(self.parameter.variable.value))


class QSAMathFrame(QSAInfoFrame):
    """A small region to display the result of a simple equation relating parameter values"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameters=[],
                 text="",
                 interval=0,
                 constants=[]
                 ):

        self.parameters = parameters
        self.constants = constants

        self.state = SubscriberVariable()
        self.state.bind_to(self.updateState)

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameters[0], text=text, interval=interval, constants=constants)
        self.setFixedWidth(105)

        self.layout.removeWidget(self.label_info)
        self.label_info.hide()
        self.layout.setContentsMargins(5, 1, 5, 1)

        self.state.value = 1
        self.state.value = 0


        if len(self.constants):
            self.layout.addWidget(self.button_expand, 0, 6)

        self.label.setFixedWidth(60)


    def poll(self):
        """Read the parameters at a regular interval"""
        for parameter in self.parameters:
            if len(parameter.command) and 'W' not in parameter.permission:
                self.master.serial.sendSerial(message = parameter.command + 'R')

    def updateState(self, value=None):
        """Change the visual appearance based on the state variable"""
        if self.state.valueprev != self.state.value:
            if self.state.value == 0:
                self.setStyleSheet(widgetStyle_mathFrameBad)
            else:
                self.setStyleSheet(widgetStyle_mathFrameGood)

    def updateValue(self, text=None):
        """Update the displayed value when the serial parameter variable changes"""
        result = 0
        try:
            result = self.equation()
            #self.label_info.setText(str(result))
        except:
            return

    def equation(self):
        """Overwrite this function in the inherited class to customize the functionality"""
        self.state.value = 0
        return self.parameters[0].variable.value


class QSAPushbutton(QSAVariableFrame):
    """A small region containing a push button"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 text=""
                 ):

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, text=text)

        self.layout.removeWidget(self.label)
        self.label.hide()

        self.button = QPushButton(self.text)
        self.button.setFixedWidth(150)
        self.button.setStyleSheet(widgetStyle_QSAPushbutton)

        self.layout.addWidget(self.button, 0, 0)

        self.button.clicked.connect(self.onClick)

    def onClick(self):
        return


class QSAToggleButton(QSAPushbutton):
    """A small region containing a button which toggles between two states"""
    def __init__(self, master=None,
                 row=0, column=0, index=0,
                 parameter=None,
                 offText = "Disabled", onText = "Enabled",
                 text=""):

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, text=offText)

        self.offText = offText
        self.onText = onText

        self._buttonText = offText
        self.state = SubscriberVariable()
        self.state.value = 0

        self.index = index

        if self.parameter is not None:
            self.command = self.parameter.command
            self.parameter.variable.bind_to(lambda val: self.updateValue(val))

        self.button.clicked.connect(lambda: self.updateValue(1-self.state.value))
        self.button.setToolTip(self.description)

    @property
    def buttonText(self):
        return self._buttonText

    @buttonText.setter
    def buttonText(self, buttonText):
        self._buttonText = buttonText
        self.button.setText(self._buttonText)

    @buttonText.getter
    def buttonText(self):
        return self._buttonText

    def updateValue(self, value):
        """Update the button state when the serial parameter variable changes"""
        self.state.value = value
        if self.state.value:
            self.button.setStyleSheet(widgetStyle_toggleButtonEnable)
            self.buttonText = self.onText
        else:
            self.button.setStyleSheet(widgetStyle_toggleButtonDisable)
            self.buttonText = self.offText

    def getWriteCommand(self):
        """Build the command to send when writing a parameter"""
        self.parameter.variable.value = self.state.value
        var = str(self.parameter.variable.value)
        if len(var) > 7:
            var = var[:7]
        return self.command + 'W' + var


class QSAToggleButtonLive(QSAToggleButton):
    """A toggle button which sends commands instantly and also polls"""
    def __init__(self, master=None,
                 serial=None, interval=0,
                 row=0, column=0, index=0,
                 parameter=None,
                 offText = "Disabled", onText = "Enabled",
                 text=""):

        super().__init__(master=master, row=row, column=column, index=index, parameter=parameter, offText=offText, onText=onText, text=text)

        self.timer = QTimer()
        self.timer.timeout.connect(self.poll)
        self.interval = interval
        self.defaultinterval = interval

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        if interval >= 100:
            self._interval = abs(interval / 1000)
        else:
            self._interval = abs(interval)
        if self._interval > 0:
            self.timer.setInterval(self._interval * 1000)
            self.timer.start()
        else:
            self.timer.setSingleShot(True)

    @interval.getter
    def interval(self):
        return self._interval

    def poll(self):
        """Read the parameter at a regular interval"""
        if len(self.parameter.command):
            self.master.serial.sendSerial(message = self.getReadCommand())

    def updateValue(self, value):
        """Update the button state and send a command when the button is pressed"""
        if value != self.state.value:
            self.state.value = value
            if len(self.parameter.command):
                self.master.serial.sendSerial(message = self.getWriteCommand())
                self.poll()
            if self.state.value:
                self.button.setStyleSheet(widgetStyle_toggleButtonEnable)
                self.buttonText = self.onText
            else:
                self.button.setStyleSheet(widgetStyle_toggleButtonDisable)
                self.buttonText = self.offText


class QSAPlusButton(QPushButton):
    """A small button with a plus on it"""
    def __init__(self):
        super().__init__()
        self.setText("+")
        self.setToolTip("Edit constants")
        self.setFixedWidth(25)
        self.setFixedHeight(25)

        self.setStyleSheet(widgetStyle_QSAPushbutton)
        #self.setGraphicsEffect(QSADropShadow(parent=self))


class QSALine(QFrame):
    """A horizontal line"""
    def __init__(self, thickness=3, color='black'):
        super().__init__()
        self.setGeometry(0,0,100,thickness*3)
        self.setFixedHeight(thickness)
        self.setStyleSheet("""
        QFrame {border-color: %s;}
        """ % color)
        self.setLineWidth(thickness)
        self.setFrameStyle(QFrame.HLine | QFrame.Plain)


class QSAImage(QLabel):
    """A static image"""
    def __init__(self, master=None, image=None):
        super().__init__()
        self.master = master
        self.image = image
        self.widget = None

    def fillImage(self):
        self.setAutoFillBackground(True)
        if self.image:
            self.pixmap = QPixmap(self.master.master.get_resource(self.image))
            self.setPixmap(self.pixmap)
            self.resize(self.pixmap.width(), self.pixmap.height())
            self.show()

    def setAdminMode(self, adminMode=False):
        self.show()