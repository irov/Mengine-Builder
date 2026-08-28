from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.FileSystem import FileSystem
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.Operation.OperationManager import OperationManager

class ResourceHandlerSoundConvertToWAV(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def convertFFMPEGToWAV(self, fileNode):
        path = fileNode.getAttribute("Path")
        pathWAV = FileSystem.setFileExtension(path, "wav")

        destination = self.fileSystemCursor.getFileDestinationPath(pathWAV)
        source = self.fileSystemCursor.getFileSourcePath(path)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('ConvertFFMPEGtoWAV', SourcePath = source, DestinationPath = destination)
            pass

        if fileNode.hasAttribute("Converter"):
            fileNode.removeAttribute("Converter")
            pass

        fileNode.setAttribute("Path", pathWAV)
        fileNode.setAttribute("Codec", "wavSound")

        self.setDocumentToRewrite()
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        self.convertFFMPEGToWAV(fileNode)

        return True
        pass
    pass
