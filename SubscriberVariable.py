class SubscriberVariable(object):
    def __init__(self):
        self._value = 0
        self.valueprev = 0
        self._observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Setting this.value triggers a list of callback functions in other classes"""
        self.valueprev = self._value
        self._value = value
        for callback in self._observers:
            callback(self._value)

    def get(self):
        return self._value

    def set(self, val):
        self._value = val

    def bind_to(self, callback):
        """Register a function to be triggered when the value of this variable changes"""
        self._observers.append(callback)
