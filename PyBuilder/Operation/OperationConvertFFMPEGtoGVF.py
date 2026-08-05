from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Toolchain import tool_path

import ToolsBuilderPlugin

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
        if ToolsBuilderPlugin.convert(self.sourcePath, self.destinationPath, "ffmpegToGVF", dict(ffmpeg=toolFile)) is False:
            ErrorHandler.warning("invalid video %s converting to %s", self.sourcePath, self.destinationPath)
            return False
            pass

        return True
        pass
    pass
