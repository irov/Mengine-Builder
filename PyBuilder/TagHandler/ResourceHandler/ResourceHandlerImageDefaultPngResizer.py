from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Environment import Environment


class ResourceHandlerImageDefaultPngResizer(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def pngOptimize(self, fileNode):
        path = fileNode.getAttribute("Path")

        if fileNode.hasAttribute("__Dir"):
            source = fileNode.getAttribute("__Dir")
            pass
        else:
            source = self.fileSystemCursor.getFileSourcePath(path)
            pass

        extension = FileSystem.getFileExtension(source)
        if extension != "png":
            return False
            pass

        parts = FileSystem.splitByExtension(path)
        newPath = parts[0] + "_resizer.png"

        project = Environment.getCurrentProject()
        temp = FileSystem.joinAndNormalisePath(project.logDir, "resizerOpt")

        dirNewPath = FileSystem.getDirname(newPath)
        tempDir = FileSystem.joinAndNormalisePath(temp, dirNewPath)

        FileSystem.makeDirsRecursiveIfNotExist(tempDir)
        tempPath = FileSystem.joinAndNormalisePath(temp, newPath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation( 'AliasPngResizer', SourcePath = source, DestinationPath = tempPath )
            pass

        fileNode.setAttribute("__Dir", tempPath)

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
