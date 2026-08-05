from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager

import ToolsBuilderPlugin

class ResourceHandlerParticle(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        path = fileNode.getAttribute("Path")

        if fileNode.hasAttribute("__Dir"):
            source = fileNode.getAttribute("__Dir")
            pass
        else:
            source = self.fileSystemCursor.getFileSourcePath(path)
            pass

        converter = ""
        if fileNode.hasAttribute("Converter"):
            converter = fileNode.getAttribute("Converter")

            fileNode.removeAttribute("Converter")
            pass

        pathPTZ = "StoreParticle/" + ToolsBuilderPlugin.pathSHA1(source) + ".ptz"

        destination = self.fileSystemCursor.getFileDestinationPath(pathPTZ)

        dirName = FileSystem.getDirname(destination)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        if converter != "":
            if ToolsBuilderPlugin.convert(source, destination, converter, {}) is False:
                print("invalid particle %s converting to %s" % (source, destination))

                return False
                pass
            pass
        else:
            with OperationManager.runOperationChain() as oc:
                oc.addOperation("CopyFile", SourcePath=source, DestinationPath=destination, Doc="ResourceHandlerParticle")
                pass

            if oc.isSuccess() is False:
                return False
            pass

        fileNode.setAttribute("Path", pathPTZ)

        return True
        pass
    pass
