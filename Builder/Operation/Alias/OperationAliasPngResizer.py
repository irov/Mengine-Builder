from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem

import os

from Builder.OSSystem import OSSystem

class OperationAliasPngResizer(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath))
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if OSSystem.tool("ffmpeg", "-loglevel", "error", "-y", "-i", self.sourcePath, "-vf", "scale=iw/2:ih/2", self.destinationPath) is False:
            return False
            pass

        return True
        pass
    pass
