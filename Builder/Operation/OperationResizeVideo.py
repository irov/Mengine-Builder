from Builder.OSSystem import OSSystem
from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem

class OperationResizeVideo(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.resize = params.pop("Resize")
        pass

    def _getInfo(self):
        return "video %s converting to %s" % (self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        scale = "scale=iw*%f:ih*%f" % (self.resize, self.resize)

        if OSSystem.tool("ffmpeg", "-loglevel", "error", "-y", "-i", self.sourcePath, "-vf", scale, self.destinationPath) is False:
            return False
            pass

        return True
        pass
    pass
