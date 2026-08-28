from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem

import os

from Builder.OSSystem import OSSystem

class OperationConvertFFMPEGtoWEBM(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return ("video %s  converting to %s" % (self.sourcePath, self.destinationPath))
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if OSSystem.tool(
            "ffmpeg", "-loglevel", "error", "-y", "-i", self.sourcePath,
            "-codec:v", "libvpx", "-f", "webm", "-qmin", "5", "-qmax", "15",
            "-threads", "4", self.destinationPath,
        ) is False:
            return False
            pass

        return True
        pass
    pass
