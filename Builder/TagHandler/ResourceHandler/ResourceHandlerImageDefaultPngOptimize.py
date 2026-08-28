from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.FileSystem import FileSystem
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.Operation.OperationManager import OperationManager
from Builder.Environment import Environment


class ResourceHandlerImageDefaultPngOptimize(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def pngOptimize(self, fileNode):
        if fileNode.hasAttribute("NoExist") and fileNode.getAttribute("NoExist") == "1":
            return
            pass

        path = fileNode.getAttribute("Path")

        if fileNode.hasAttribute("__Dir"):
            source = fileNode.getAttribute("__Dir")
            pass
        else:
            source = self.fileSystemCursor.getFileSourcePath(path)
            pass

        extension = FileSystem.getFileExtension(source)

        if extension != "png":
            return
            pass

        parts = FileSystem.splitByExtension(path)
        newPath = parts[0] + "_opt.png"

        project = Environment.getCurrentProject()
        temp = FileSystem.joinAndNormalisePath(project.logDir, self.pakName + "_pngOpt")

        dirNewPath = FileSystem.getDirname(newPath)
        tempDir = FileSystem.joinAndNormalisePath(temp, dirNewPath)

        FileSystem.makeDirsRecursiveIfNotExist(tempDir)
        tempPath = FileSystem.joinAndNormalisePath(temp, newPath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('AliasSafetyPngOptimize', SourcePath=source, DestinationPath=tempPath)
            pass

        fileNode.setAttribute("Path", newPath)
        fileNode.setAttribute("__Dir", tempPath)

        if project.imagePremultiply is True:
            fileNode.setAttribute("Premultiply", "1")
            pass

        self.setDocumentToRewrite()
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        self.pngOptimize(fileNode)

        return True
        pass
    pass
