from PyBuilder.Arguments.Argument import Argument

class ArgumentBool(Argument):
    def _getInfo(self):
        return "Possible values : disable or enable"
        pass

    def _getData(self, argName, argValue):
        if argValue == "enable" or argValue == "true" or argValue:
            self.value = True
            return True
            pass
        elif argValue == "disable" or argValue == "false" or not argValue:
            self.value = False
            return True
            pass

        return False
        pass

    pass
