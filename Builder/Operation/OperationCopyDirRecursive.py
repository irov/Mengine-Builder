from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem


class OperationCopyDirRecursive(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.ignoredPatterns = params.pop("IgnoredPatterns", None) #('.svn')
        self.copyFileCallback = params.pop("CopyFileCallback", None)
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath))
        pass

    def _onRun(self):
        if self.sourcePath == self.destinationPath:
            message = "Critical Bug baseDir %s == targetDir in %s operation" % (self.sourcePath , self)
            ErrorHandler.error(message)
            return False
            pass

        dirName = FileSystem.getDirname(self.destinationPath)

        #Fix ME
        if FileSystem.isDirectory(dirName) is False:
            FileSystem.makeDirsRecursive(dirName)
            pass

        try:
            FileSystem.copyDirRecursive(self.sourcePath, self.destinationPath, copyFileFunction=self.copyFileCallback, ignorePatterns=self.ignoredPatterns)
        except BaseException as ex:
            print("Exception:", ex)
            print("Source:", self.sourcePath)
            print("Destination:", self.destinationPath)

            return False
            pass

        return True
        pass
    pass
