from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem
from Builder.Toolchain import tool_path

from Builder import Tools

class OperationConvertFFMPEGtoOGVA(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        self.resize = params.pop("Resize")
        pass

    def _getInfo(self):
        return "video %s converting to %s" % (self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        ffmpeg = tool_path("ffmpeg")
        quality = self.quality // 10

        if Tools.convert(self.sourcePath, self.destinationPath, "ffmpegToOGVA", dict(ffmpeg=ffmpeg, quality=quality, resize=self.resize)) is False:
            print("invalid video %s converting to %s" % (self.sourcePath, self.destinationPath))
            return False
            pass

        return True
        pass
    pass
