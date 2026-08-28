from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
from Builder.Operation.Operation import Operation


class OperationCopyFile(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        if params.get("Doc", "") == "ResourceHandler":
            self.exist = params.get("Exist", False)
        else:
            self.exist = params.get("Exist", True)
        self.Doc = params.get("Doc", "")
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath  ) )
        pass

    def _onRun(self):
        if self.sourcePath == self.destinationPath:
            message = "Critical Bug baseFile %s == targetFile in copy operation" % self.sourcePath
            ErrorHandler.error(message)
            return False
            pass

        if FileSystem.isFile(self.sourcePath) is False:
            if self.exist is False:
                ErrorHandler.warning("break OperationCopyFile '%s' is not found", self.sourcePath)
                return True
                pass
            else:
                message = "Critical Bug baseFile %s not exist! [%s]" % (self.sourcePath, self.Doc)
                ErrorHandler.error(message)
                return False
                pass
            pass

        if FileSystem.isAccess(self.sourcePath) is False:
            if self.exist is False:
                ErrorHandler.warning("break OperationCopyFile '%s' is not access", self.sourcePath)
                return True
                pass
            else:
                message = "Critical Bug baseFile %s not access! [%s]" % (self.sourcePath, self.Doc)
                ErrorHandler.error(message)

                return False
                pass
            pass

        #FixMe
        dirName = FileSystem.getDirname(self.destinationPath)
        if FileSystem.isDirectory(dirName) == False and dirName != '':
            FileSystem.makeDirsRecursive(dirName)
            pass

        FileSystem.copyFile(self.sourcePath,self.destinationPath)

        return True
        pass
    pass
