from PyBuilder.Arguments.Argument import Argument

class ArgumentMulti(Argument):
    def __init__(self, argName, description, possibleValues):
        super(ArgumentMulti,self).__init__(argName, description)
        self.possibleValues = possibleValues
        pass

    def _getData(self, argName, argValue):
        for possiblePair in self.possibleValues:
            check = possiblePair[0]
            if check == argValue:
                self.value = possiblePair[1]
                return True
                pass
            pass

        return False
        pass
    pass
