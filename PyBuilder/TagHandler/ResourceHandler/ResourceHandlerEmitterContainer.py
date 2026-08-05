__author__ = 'human88998999877'
from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager

class ResourceHandlerEmitterContainer(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        path = fileNode.getAttribute("Path")

        destination = self.fileSystemCursor.getFileDestinationPath(path)

        if fileNode.hasAttribute("__Dir"):
            source = fileNode.getAttribute("__Dir")
            pass
        else:
            source = self.fileSystemCursor.getFileSourcePath(path)
            pass

        destinationDirName = FileSystem.getDirname(destination)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyFile", SourcePath = source, DestinationPath = destination, Doc="ResourceHandlerEmitterContainer")

            oc.addOperation("AstralaxParse", SourcePath = source, DestinationPath = destinationDirName)
            pass

        return oc.isSuccess()
        pass
    pass
