from PyBuilder.Operation.Operation import Operation
from PyBuilder.FileSystem import FileSystem

from PyBuilder import Tools

class OperationConvertImageToHTF(Operation):
    def _getInfo(self):
        return ("image %s  converting  to  HTF   %s" % (self.sourcePath, self.destinationPath))
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        self.codec = params.pop("Codec")
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if Tools.convert(self.sourcePath, self.destinationPath, self.codec, {}) is False:
            print("invalid image %s converting to %s" % (self.sourcePath, self.destinationPath))
            return False
            pass

        return True
        pass
    pass
