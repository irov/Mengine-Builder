from Builder.TagHandler.TagHandler import TagHandler
from Builder.Operation.OperationManager import OperationManager

class TagHandlerFile(TagHandler):
    def copyFile(self, sourcePath, destinationPath):
        sourceFull = self.fileSystemCursor.getFileSourcePath(sourcePath)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destinationPath)

        if sourceFull != destinationFull:
            with OperationManager.runOperationChain() as oc:
                oc.addOperation( 'CopyFile', SourcePath=sourceFull, DestinationPath=destinationFull, Doc="TagHandlerFile")
                pass
            pass

        return oc.isSuccess()
        pass

    def _onExecute(self):
        path = self.node.getAttribute("Path")
        if self.copyFile(path, path) is False:
            return False
            pass

        return True
        pass
    pass
