from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem

class OperationRemoveDirRecursive(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        pass

    def _getInfo(self):
        return "source  %s"%(self.sourcePath)
        pass

    def _onRun(self):
        FileSystem.removeDirRecursive(self.sourcePath)

        return True
        pass
