from Builder.Arguments.Argument import Argument

class ArgumentFloat(Argument):
    def _getData(self, argName, argValue):
        try:
            self.value = float(argValue)
            pass
        except BaseException as e:
            return False
            pass

        return True
        pass
    pass
