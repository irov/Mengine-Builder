from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
from Builder.Toolchain import tool_path

from Builder import Tools

class OperationConvertFFMPEGtoGVF(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return "video %s converting to %s" % (self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        toolFile = tool_path("ffmpeg")
        if Tools.convert(self.sourcePath, self.destinationPath, "ffmpegToGVF", dict(ffmpeg=toolFile)) is False:
            ErrorHandler.warning("invalid video %s converting to %s", self.sourcePath, self.destinationPath)
            return False
            pass

        return True
        pass
    pass
