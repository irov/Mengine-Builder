from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
import os

from Builder.OSSystem import OSSystem

class OperationConvertImageToDDS(Operation):
    def _getInfo(self):
        return ("image %s  converting  to DDS %s" % (self.sourcePath, self.destinationPath ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        self.format = params.pop("Format")
        pass

    def _onRun(self):
        #FixME
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        quality = float(self.quality) / 100.0 * 255.0

        if OSSystem.tool(
            "crunch", "-quiet", "-file", self.sourcePath, "-out", self.destinationPath,
            "-fileformat", "dds", "-" + self.format, "-mipMode", "None", "-quality", str(quality),
        ) is False:
            return False
            pass

        return True
        pass
    pass
