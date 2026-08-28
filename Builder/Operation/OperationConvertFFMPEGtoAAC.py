from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem
import os

from Builder.OSSystem import OSSystem

class OperationConvertFFMPEGtoAAC(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return "ffmpeg %s converting to %s"%(self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        #FixME
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if OSSystem.tool(
            "ffmpeg", "-loglevel", "error", "-y", "-i", self.sourcePath,
            "-map_metadata:g", "-1:g", "-map_metadata:s:v", "-1:g",
            "-map_metadata:s:a", "-1:g", self.destinationPath,
        ) is False:
            return False
            pass

        return True
        pass
    pass
