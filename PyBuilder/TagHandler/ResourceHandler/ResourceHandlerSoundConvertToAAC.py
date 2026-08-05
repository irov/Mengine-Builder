from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager

class ResourceHandlerSoundConvertToAAC(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def convertFFMPEGToAAC(self, fileNode):
        path = fileNode.getAttribute("Path")
        pathAAC = FileSystem.setFileExtension(path, "aac")

        destination = self.fileSystemCursor.getFileDestinationPath(pathAAC)
        source = self.fileSystemCursor.getFileSourcePath(path)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('ConvertFFMPEGtoAAC', SourcePath = source, DestinationPath = destination)
            pass

        if fileNode.hasAttribute("Converter"):
            fileNode.removeAttribute("Converter")
            pass

        fileNode.setAttribute("Path", pathAAC)
        fileNode.setAttribute("Codec", "aacSound")

        self.setDocumentToRewrite()
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        self.convertFFMPEGToAAC(fileNode)

        return True
        pass
    pass
