from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvert import ResourceHandlerImageConvert
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.OperationManager import OperationManager

from PyBuilder.Environment import Environment

class ResourceHandlerImageConvertToWEBP(ResourceHandlerImageConvert):
    def _process(self, fullPath, fileNode, NoAtlas, IsAtlas):
        project = Environment.getCurrentProject()

        filename = fileNode.getAttribute("Path")

        PathWEBP = FileSystem.setFileExtension(filename, "webp")

        MakeAtlas = project.isMakeAtlas is True and NoAtlas is False and IsAtlas is True

        if MakeAtlas is True:
            self.node.setAttribute("Name", PathWEBP)
            pass

        fileNode.setAttribute("Codec", "webpImage")
        fileNode.setAttribute("Path", PathWEBP)

        destinationFull = self.fileSystemCursor.getFileDestinationPath(PathWEBP)

        imageConvertQuality = project.imageConvertQuality

        if self.pool.imageQuality is not None:
            imageConvertQuality = int(self.pool.imageQuality)
            pass

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('ConvertImageToWEBP'
                , SourcePath=fullPath
                , DestinationPath=destinationFull
                , Quality=imageConvertQuality
                , Trim=False
            )
            pass

        if oc.isSuccess() is False:
            return False
            pass

        return True
        pass
    pass
