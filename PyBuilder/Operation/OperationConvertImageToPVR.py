from PyBuilder.Operation.Operation import Operation
from PyBuilder.FileSystem import FileSystem

from PyBuilder.OSSystem import OSSystem

class OperationConvertImageToPVR(Operation):
    def _getInfo(self):
        return ("image %s  converting  to PVR %s" % (self.sourcePath, self.destinationPath ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        self.format = params.pop("Format")
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        #quality = "pvrtcbest" if int(self.quality) != 0 else "pvrtcfastest"
        quality = "pvrtcfastest"

        if OSSystem.tool("PVRTexToolCLI", "-i", self.sourcePath, "-o", self.destinationPath, "-f", self.format, "-dither", "-q", quality) is False:
            return False
            pass

        return True
        pass
    pass
