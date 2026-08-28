from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.Operation.OperationManager import OperationManager

class ResourceHandlerMovie2(ResourceHandler):
    def _onExecute(self):
        Path = self.node.getChildAttribute("File", "Path")

        PathSource = self.fileSystemCursor.getFileSourcePath(Path)
        PathDestination = self.fileSystemCursor.getFileDestinationPath(Path)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyFile", SourcePath = PathSource, DestinationPath = PathDestination, Doc="ResourceHandlerMovie2")
            pass

        return True
        pass
    pass
