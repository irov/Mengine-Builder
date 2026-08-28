from Builder.Arguments.Argument import Argument


class ArgumentString(Argument):
    def _getData(self, argName, argValue):
        self.value = argValue
        return True
        pass
    pass
