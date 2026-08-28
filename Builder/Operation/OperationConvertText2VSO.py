from Builder.Operation.Operation import Operation

from Builder.FileSystem import FileSystem

from Builder import Tools

class OperationConvertText2VSO(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return "fxc %s converting to %s"%(self.sourcePath, self.destinationPath)
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if Tools.convert(self.sourcePath, self.destinationPath, "text2vso", {}) is False:
            print("invalid sound %s converting to %s"%(self.sourcePath, self.destinationPath))
            return False
            pass

        return True
        pass
    pass
