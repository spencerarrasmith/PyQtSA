import math
from pyqtsa.SubscriberVariable import SubscriberVariable

MAX_LEN_UNITS = 4
MAX_PRECISION = 8


class GUIParameter(object):
    """
    A database object which contains all relevant information about a serial parameter as well as a subscriber variable
    """
    def __init__(self,
                 name="",
                 command="",
                 permission="",
                 description="",
                 param_type="",
                 mode="",
                 group="",
                 units="",
                 value_min=-math.inf,
                 value_max=math.inf,
                 precision=0,
                 scale=1
                 ):
        self._name = name
        self._command = command
        self._permission = permission
        self._description = description
        self._param_type = param_type
        self._mode = mode
        self._group = group
        self._units = units
        self._value_min = value_min
        self._value_max = value_max
        self._precision = precision
        self._scale = scale

        self.variable = SubscriberVariable()
        self.state = None

    # Name - the name of the command
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        print(self._name)

    @name.getter
    def parameter(self):
        return self._name

    # Command - Callback command which is sent
    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        self._command = command
        print(self._command)

    @command.getter
    def command(self):
        return self._command

    # Permission - read/write/protected to specify command access
    @property
    def permission(self):
        return self._permission

    @permission.setter
    def permission(self, permission):
        self._permission = permission

    @permission.getter
    def permission(self):
        return self._permission

    # Description - a text description of the parameter
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @description.getter
    def description(self):
        return self._description

    # Type - the data type for the associated variable
    @property
    def param_type(self):
        return self._param_type

    @param_type.setter
    def param_type(self, param_type):
        self._param_type = param_type
        if self.permission.upper() in ['RW', 'WR', 'PRW', 'PWR']:
            if self._param_type == "BOOL":
                self._value_min = 0
                self._value_max = 1
                self.precision = 0
            elif self._param_type in ["U8", "U16", "U32", "I8", "I16", "I32"]:
                self.precision = 0
            elif self._param_type in ["FLOAT", "DOUBLE"]:
                self.mode = "FIX"

        elif self.permission.upper() == "R":
            if self._param_type == "STRING":
                self.variable.value = ""
                return
            else:
                return

    @param_type.getter
    def param_type(self):
        return self._param_type

    # Mode - the textual representation of the variable, e.g. ENUM for a U8
    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        if self.mode == "ENUM":
            #self.state = SubscriberVariable()
            return

    @mode.getter
    def mode(self):
        return self._mode

    # Group - the functional group of the command
    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group

    @group.getter
    def group(self):
        return self._group

    # Units - a string specifying the variable's units
    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = units
        if len(self.units) > MAX_LEN_UNITS:
            self._units = self.units[0:MAX_LEN_UNITS]

    @units.getter
    def units(self):
        return self._units

    # Min - the minimum value
    @property
    def value_min(self):
        return self._value_min

    @value_min.setter
    def value_min(self, value_min):
        if value_min <= self._value_max:
            self._value_min = value_min
        else:
            self._value_min = self._value_max
        if self._param_type in ["U8", "U16", "U32", "I8", "I16", "I32"]:
            self._value_min = int(self._value_min)

    @value_min.getter
    def value_min(self):
        return self._value_min

    # Max - the maximum value
    @property
    def value_max(self):
        return self._value_max

    @value_max.setter
    def value_max(self, value_max):
        if value_max >= self._value_min:
            self._value_max = value_max
        else:
            self._value_max = self.value_min
        if self._param_type in ["U8", "U16", "U32", "I8", "I16", "I32"]:
            self._value_max = int(self._value_max)

    @value_max.getter
    def value_max(self):
        return self._value_max

    # Precision - decimal precision for the variable
    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, precision):
        self._precision = precision
        if self.precision >= 0 :
            if self.precision <= MAX_PRECISION:
                self._precision = precision
            else:
                self._precision = MAX_PRECISION
        else:
            self._precision = 0

    @precision.getter
    def precision(self):
        return self._precision

    # Scale - sets a scale hidden to the user, e.g. user sees 1 but GUI sends 1000000
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        if self.scale != 0:
            self._scale = scale
            self._value_min /= self.scale
            self._value_max /= self.scale

    @scale.getter
    def scale(self):
        return self._scale
