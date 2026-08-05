from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager


class ResourceHandlerImageConvertToHit(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def convertPNGToHIT(self,fileNode):
        path = fileNode.getAttribute("Path")
        pathHIT = FileSystem.setFileExtension(path,"hit")

        destinationHIT = self.fileSystemCursor.getFileDestinationPath(pathHIT)
        source = self.fileSystemCursor.getFileSourcePath(path)

        with OperationManager.runOperationChain() as oc:
            #oc.addOperation( 'copyFile', SourcePath = source, DestinationPath = destination )
            oc.addOperation( 'convertPNGToHIT', SourcePath = source, DestinationPath = destinationHIT )
            pass


        if fileNode.hasAttribute("Converter"):
            fileNode.removeAttribute("Converter")
            fileNode.setAttribute("Codec", "hitPick")
            pass

        fileNode.setAttribute("Path",pathHIT)
        self.setDocumentToRewrite()
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Converter") is False:
            path = fileNode.getAttribute("Path")
            self.copyFile(path, path)
            pass
        else:
            converter = fileNode.getAttribute("Converter")
            self.convertPNGToHIT(fileNode)
            pass

        return True
        pass
    pass
