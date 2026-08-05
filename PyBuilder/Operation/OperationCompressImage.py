from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
import os

from PyBuilder.OSSystem import OSSystem

class OperationCompressImage(Operation):
    def _getInfo(self):
        return ("image %s  compressed " % (self.sourcePath ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationDir = params.pop("DestinationDirectory")
        pass

    def _onRun(self):
        if OSSystem.tool(
            "crunch", "-file", self.sourcePath, "-outdir", self.destinationDir,
            "-fileformat", "dds", "-dxt1", "-quality", "100", "-mipmode", "none",
        ) is False:
            return False
            pass

        FileSystem.removeFile(self.sourcePath)

        return True
        pass
        pass
    pass
