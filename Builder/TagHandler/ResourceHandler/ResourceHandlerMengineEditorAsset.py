from Builder.Operation.OperationManager import OperationManager
from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler


class ResourceHandlerMengineEditorAsset(ResourceHandler):
    def __init__(self, assetType):
        super(ResourceHandlerMengineEditorAsset, self).__init__()
        self.assetType = assetType
        pass

    def _onExecute(self):
        source = self.node.getChildAttribute("Source", "Path")
        destination = self.node.getChildAttribute("File", "Path")
        sourceFull = self.fileSystemCursor.getFileSourcePath(source)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destination)

        with OperationManager.runOperationChain() as operationChain:
            operationChain.addOperation(
                "CompileMengineEditorAsset",
                SourcePath=sourceFull,
                DestinationPath=destinationFull,
                AssetType=self.assetType,
            )
            pass

        return True

