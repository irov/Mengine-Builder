from Builder import Tools

from Builder.Operation.Operation import Operation
from Builder.FileSystem import FileSystem

class OperationCopyHitFile(Operation):
    def _onParams( self, params ):
       self.sourcePath = params.pop("SourcePath")
       self.destinationPath = params.pop("DestinationPath")
       pass

    def _onRun(self):
        dirname = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirname)

        if Tools.convert(self.sourcePath, self.destinationPath, "png2hit", {}) is False:
            print("invalid hit %s converting to %s" % (self.sourcePath, self.destinationPath))
            return False
            pass

        return True
        pass
    pass
