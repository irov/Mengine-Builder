from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.Operation import Operation
from PyBuilder.FileSystem import FileSystem
import os

from PyBuilder.OSSystem import OSSystem

class OperationYamdiOptimize (Operation):
    def _onParams( self, params ):
       self.sourcePath = params.pop("SourcePath")
       self.destinationPath = params.pop("DestinationPath")
       pass

    def _onRun(self):
        dirname = FileSystem.getDirname(self.sourcePath)
        FileSystem.makeDirsRecursiveIfNotExist(dirname)
        if OSSystem.tool("yamdi", "-i", self.sourcePath, "-M", "-o", self.destinationPath) is False:
            return False
            pass

        return True
        pass
    pass
