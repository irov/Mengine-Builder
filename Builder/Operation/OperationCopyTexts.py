from Builder.Operation.Operation import Operation
from Builder.Operation.OperationManager import OperationManager

from Builder import Compile

class OperationCopyTexts(Operation):
    def _onParams( self, params ):
        self.Path = params.pop("Path")
        self.fileSystemCursor = params.pop("fileSystemCursor")
        pass

    def copyFile(self, sourcePath, destinationPath):
        sourceFull = self.fileSystemCursor.getFileSourcePath(sourcePath)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destinationPath)

        if sourceFull != destinationFull:
            with OperationManager.runOperationChain() as oc:
                oc.addOperation('CopyFile', SourcePath=sourceFull, DestinationPath=destinationFull, Doc="OperationCopyTexts")
                pass
            pass

        return oc.isSuccess()
        pass

    def _getInfo(self):
        return ("source %s" % (self.Path))
        pass

    def _onRun(self):
        self.copyFile(self.Path, self.Path)

        return True
        pass
