from PyBuilder.Arguments.Argument import Argument

class ArgumentList(Argument):
    def __init__(self, argName, description, important=True, default=None):
        if default is None:
            default = []

        super().__init__(argName, description, important=important, default=default)
        pass

    def _getData(self, argName, argValue):

        if type(argValue) == str:
            argValue = argValue.split()

        self.value = argValue
        return True
        pass
