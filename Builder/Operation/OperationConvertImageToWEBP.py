from Builder.Operation.Operation import Operation
from Builder.FileSystem import FileSystem

from Builder.OSSystem import OSSystem

class OperationConvertImageToWEBP(Operation):
    def _getInfo(self):
        return ("image %s  converting  to  WEBP   %s" % (self.sourcePath, self.destinationPath ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        self.trim = params.pop("Trim")
        self.NoAlpha = params.pop("NoAlpha", False)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        crop_data = None
        if self.trim is True:
            crop_data = self.doTrim()
            pass

        arguments = ["-mt", "-quiet"]
        if self.NoAlpha is True:
            arguments.append("-noalpha")

        arguments.extend(("-q", str(self.quality)))

        if crop_data is not None:
            arguments.extend(("-crop", str(crop_data[4]), str(crop_data[5]), str(crop_data[2]), str(crop_data[3])))

        arguments.extend((self.sourcePath, "-o", self.destinationPath))

        if OSSystem.tool("cwebp", *arguments) is False:
            return False

        return True

    def doTrim(self):
        returncode, result = OSSystem.process_tool("ImageTrimmer", ("--in_path", self.sourcePath, "--trim", "1"))

        if returncode != 0:
            raise RuntimeError("ImageTrimmer failed for '%s'" % self.sourcePath)

        data = result.split("\n")

        width = int(data[0])
        height = int(data[1])
        new_width = int(data[2])
        new_height = int(data[3])
        offset_i = int(data[4])
        offset_j = int(data[5])

        return [width, height, new_width, new_height, offset_i, offset_j]
        pass
    pass
