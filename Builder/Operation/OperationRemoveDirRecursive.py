from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem

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
