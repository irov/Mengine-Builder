from PyBuilder.Operation.Operation import Operation

from PyBuilder.FileSystem import FileSystem
from PyBuilder.Toolchain import tool_path

import ToolsBuilderPlugin

class OperationConvertFFMPEGtoOGG(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        pass

    def _getInfo(self):
        return "sound %s converting to %s" % (self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        ffmpeg = tool_path("ffmpeg")
        aq = self.quality // 10

        if ToolsBuilderPlugin.convert(self.sourcePath, self.destinationPath, "ffmpegToOggSound", dict(ffmpeg=ffmpeg, aq=aq)) is False:
            ErrorHandler.warning("invalid sound %s converting to %s", self.sourcePath, self.destinationPath)
            return False
            pass

        return True
        pass
    pass
