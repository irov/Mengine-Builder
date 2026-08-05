from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.OperationManager import OperationManager

from PyBuilder.Environment import Environment

#attach this to  "ResourceImageDefault" or checkAttributeType == "ResourceImageInAtlasCombineRGBAndAlpha"
class ResourceHandlerCopy(ResourceHandler):
    def _onExecute(self):
        self.workWithFileNodes()

        return True
        pass

    def _workWithFileNode(self, fileNode):
        filename = fileNode.getAttribute("Path")

        if fileNode.hasAttribute("__Dir"):
            sourceFull = fileNode.getAttribute("__Dir")
            pass
        else:
            sourceFull = self.fileSystemCursor.getFileSourcePath(filename)
            pass

        destinationFull = self.fileSystemCursor.getFileDestinationPath(filename)

        self.copyFile(sourceFull, destinationFull)

        return True
        pass
    pass
