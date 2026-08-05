from PyBuilder.Operation.Operation import Operation

from PyBuilder.FileSystem import FileSystem

import ToolsBuilderPlugin

class OperationConvertText2PSO(Operation):
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

        if ToolsBuilderPlugin.convert(self.sourcePath, self.destinationPath, "text2pso", {}) is False:
            print("invalid sound %s converting to %s"%(self.sourcePath, self.destinationPath))
            return False
            pass

        return True
        pass
    pass
