from Builder.Operation.Operation import Operation
from Builder.FileSystem import FileSystem

from Builder import Tools

class OperationConvertImageToACF(Operation):
    def _getInfo(self):
        return ("image %s  converting  to  ACF   %s" % (self.sourcePath, self.destinationPath ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if Tools.convert(self.sourcePath, self.destinationPath, "png2acf", {}) is False:
            print("invalid image %s converting to %s" % (self.sourcePath, self.destinationPath))
            return False
            pass

        return True
        pass
    pass
