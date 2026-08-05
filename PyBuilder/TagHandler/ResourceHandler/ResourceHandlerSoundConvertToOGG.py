from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager

from PyBuilder import Tools

class ResourceHandlerSoundConvertToOGG(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def convertFFMPEGToOGG(self, fileNode):
        path = fileNode.getAttribute("Path")

        quality = self.project.soundConvertQuality

        if fileNode.hasAttribute("Converter") and fileNode.getAttribute("Converter") == "ffmpegToOggSound":
            source = self.fileSystemCursor.getFileSourcePath(path)

            pathOGG = "StoreSound/" + Tools.pathSHA1(source) + ".ogg"

            destination = self.fileSystemCursor.getFileDestinationPath(pathOGG)

            quality = self.project.soundConvertQuality

            with OperationManager.runOperationChain() as oc:
                oc.addOperation('ConvertFFMPEGtoOGG', SourcePath=source, DestinationPath=destination, Quality=quality)
                pass

            if fileNode.hasAttribute("Converter"):
                fileNode.removeAttribute("Converter")
                pass

            fileNode.setAttribute("Path", pathOGG)
            fileNode.setAttribute("Codec", "oggSound")

            self.setDocumentToRewrite()
        elif fileNode.hasAttribute("Codec") and fileNode.getAttribute("Codec") == "oggSound" and quality != 100:
            source = self.fileSystemCursor.getFileSourcePath(path)
            destination = self.fileSystemCursor.getFileDestinationPath(path)

            quality = self.project.soundConvertQuality

            with OperationManager.runOperationChain() as oc:
                oc.addOperation('ConvertFFMPEGtoOGG', SourcePath=source, DestinationPath=destination, Quality=quality)
                pass

            self.setDocumentToRewrite()
        else:
            if fileNode.hasAttribute("Converter"):
                print("Wrong converter attribute, %s" % (fileNode.getAttribute("Converter")))
                return False
                pass

            self.copyFile(path, path)
            pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        self.convertFFMPEGToOGG(fileNode)

        return True
        pass
    pass
