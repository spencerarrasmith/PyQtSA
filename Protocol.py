import math
from .GUIParameter import GUIParameter


class Protocol:
    """
    A database comprised of GUIParameters which contains all information about all valid commands
    Implement your own protocol class that implements this one, and then fill yours out according to your design
    """
    def __init__(self, master=None):
        self.master = master
        self.parameters = {}

        """
        NOTE: Follow this example below to add all of your parameters
        
        self.addParameter(parameter="Asdf")
        self.parameters["Asdf"].name = 'RW'
        self.parameters["Asdf"].param_type = 'FLOAT'
        self.parameters["Asdf"].description = 'Testing'
        self.parameters["Asdf"].mode = 'FIX'
        self.parameters["Asdf"].group = 'Test'
        self.parameters["Asdf"].units = '%'
        self.parameters["Asdf"].value_min = 0
        self.parameters["Asdf"].value_max = 100
        self.parameters["Asdf"].precision = 3
        self.parameters["Asdf"].scale = 1
        """

    def addParameter(
            self,
            name="",  # name of this param
            command="",  # callback command to be run when this changes
            permission="RW",  # Read/Write permissions for this param
            description="",  # long-form description of this param
            param_type="",  # type of data for this param,
                            # one of ["FLOAT", "DOUBLE", "BOOL", "STRING",
                            # "U8", "U16", "U32", "U64", "I8", "I16", "I32", "I64"]
            mode="",  # TODO perhaps unused
            group="",  # internally useful method to group together parameters
            units="",  # unit description for this parameter (currently un-parsed)
            value_min=-math.inf,  # minimum possible value to constrain input
            value_max=math.inf,  # maximum possible value to constrain input
            precision=0,  # decimal points beyond zero to maintain
            scale=1  # internal scale between presented value and value kept internally
    ):
        self.parameters[name] = GUIParameter(
            name,
            command,
            permission,
            description,
            param_type,
            mode,
            group,
            units,
            value_min,
            value_max,
            precision,
            scale
        )
