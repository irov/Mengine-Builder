from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler

from PyBuilder import PyCompile

class OperationCompilePyFile(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        # self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return ("source %s" % (self.sourcePath))
        pass

    def _onRun(self):
        if PyCompile.compile27(self.sourcePath) is False:
            ErrorHandler.warning("invalid compile27 [%s]", self.__repr__())

            return False
            pass

        return True
        pass
        pass
