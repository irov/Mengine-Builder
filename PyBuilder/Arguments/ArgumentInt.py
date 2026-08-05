from PyBuilder.Arguments.Argument import Argument

class ArgumentInt(Argument):
    def _getData(self, argName, argValue):
        try:
            self.value = int(argValue)
            pass
        except BaseException as e:
            return False
            pass

        return True
        pass
    pass
