from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem
from Builder.OSSystem import OSSystem

import os
import tempfile

class OperationConvertText2Metallib(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return "xcrun metal %s converting to %s" % (self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        tempDir = tempfile.mkdtemp()
        airPath = os.path.join(tempDir, "shader.air")

        try:
            success, stdout, stderr = OSSystem.run([
                "xcrun", "-sdk", "iphoneos", "metal",
                "-c", self.sourcePath,
                "-o", airPath
            ])

            if success is False:
                print("invalid metal compile %s: %s" % (self.sourcePath, stderr))
                return False
                pass

            success, stdout, stderr = OSSystem.run([
                "xcrun", "-sdk", "iphoneos", "metallib",
                airPath,
                "-o", self.destinationPath
            ])

            if success is False:
                print("invalid metallib link %s: %s" % (airPath, stderr))
                return False
                pass
        finally:
            if os.path.exists(airPath):
                os.remove(airPath)
                pass
            if os.path.exists(tempDir):
                os.rmdir(tempDir)
                pass
            pass

        return True
        pass
    pass
