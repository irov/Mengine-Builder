from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.Operation.OperationManager import OperationManager

class ResourceHandlerSpine(ResourceHandler):
    def _onExecute(self):
        SkeletonPath = self.node.getChildAttribute("Skeleton", "Path")

        SkeletonPathSource = self.fileSystemCursor.getFileSourcePath(SkeletonPath)
        SkeletonPathDestination = self.fileSystemCursor.getFileDestinationPath(SkeletonPath)

        AtlasPath = self.node.getChildAttribute("Atlas", "Path")

        AtlasPathSource = self.fileSystemCursor.getFileSourcePath(AtlasPath)
        AtlasPathDestination = self.fileSystemCursor.getFileDestinationPath(AtlasPath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyFile", SourcePath=SkeletonPathSource, DestinationPath=SkeletonPathDestination, Doc="SkeletonPathDestination")
            oc.addOperation("CopyFile", SourcePath=AtlasPathSource, DestinationPath=AtlasPathDestination, Doc="AtlasPathDestination")
            pass

        return oc.isSuccess()
        pass
    pass
