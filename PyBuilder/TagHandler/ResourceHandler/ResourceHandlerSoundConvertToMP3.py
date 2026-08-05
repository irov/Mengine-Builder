from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager

class ResourceHandlerSoundConvertToMP3(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def convertFFMPEGToMP3(self, fileNode):
        path = fileNode.getAttribute("Path")
        pathMP3 = FileSystem.setFileExtension(path, "mp3")

        destination = self.fileSystemCursor.getFileDestinationPath(pathMP3)
        source = self.fileSystemCursor.getFileSourcePath(path)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('ConvertFFMPEGtoMP3', SourcePath = source, DestinationPath = destination)
            pass

        if fileNode.hasAttribute("Converter"):
            fileNode.removeAttribute("Converter")
            pass

        fileNode.setAttribute("Path", pathMP3)
        fileNode.setAttribute("Codec", "mp3Sound")

        self.setDocumentToRewrite()
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        self.convertFFMPEGToMP3(fileNode)

        return True
        pass
    pass
