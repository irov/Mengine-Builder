from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler

from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.OperationManager import OperationManager

from PyBuilder import Tools

class ResourceHandlerMusicConvert(ResourceHandler):
    def convertFFMPEG(self, fileNode, ext, operation, codec, **params):
        External = False
        if fileNode.hasAttribute("External"):
            if fileNode.getAttribute("External") == "1":
                External = True
                pass
            pass

        path = fileNode.getAttribute("Path")

        source = self.fileSystemCursor.getFileSourcePath(path)

        pathConvert = None

        if External is True:
            pathConvert = FileSystem.setFileExtension(path, ext)
            pathConvert = FileSystem.joinPath("External", pathConvert)

            destination = self.fileSystemCursor.getFileExportPath(pathConvert)
            pass
        else:
            pathConvert = "StoreMusic/" + Tools.pathSHA1(source) + "." + ext

            destination = self.fileSystemCursor.getFileDestinationPath(pathConvert)
            pass

        with OperationManager.runOperationChain() as oc:
            oc.addOperation(operation, SourcePath=source, DestinationPath=destination, **params)
            pass

        if fileNode.hasAttribute("Converter"):
            fileNode.removeAttribute("Converter")
            pass

        fileNode.setAttribute("Path", pathConvert)
        fileNode.setAttribute("Codec", codec)

        self.setDocumentToRewrite()
        pass

    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False
            pass

        return True
        pass
    pass
