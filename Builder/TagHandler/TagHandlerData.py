from Builder.TagHandler.TagHandler import TagHandler
from Builder.Operation.OperationManager import OperationManager

class TagHandlerData(TagHandler):
    def _onExecute(self):
        path = self.node.getAttribute("Path")

        SourcePath = self.fileSystemCursor.getFileSourcePath(path)
        DestinationPath = self.fileSystemCursor.getFileDestinationPath(path)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyFile", SourcePath=SourcePath, DestinationPath=DestinationPath, Exist=False, Doc="TagHandlerData")
            pass

        return oc.isSuccess()
        pass
    pass
