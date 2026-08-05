from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Operation.OperationManager import OperationManager

class ResourceHandler(TagHandler):
    def workWithFileNodes(self):
        files = self.node.getChildrenByTag("File")
        for fileNode in files:
            if self.workWithFileNode(fileNode) is False:
                return False
                pass
            pass

        return True
        pass

    def workWithFileNode(self, fileNode):
        return self._workWithFileNode(fileNode)
        pass

    def _workWithFileNode(self, fileNode):
        raise BaseException("Abstract")

        return False
        pass

    def copyFile(self, sourcePath, destinationPath):
        sourceFull = self.fileSystemCursor.getFileSourcePath(sourcePath)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destinationPath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('CopyFile', SourcePath=sourceFull, DestinationPath=destinationFull, Doc="ResourceHandler")
            pass
        pass
    pass
