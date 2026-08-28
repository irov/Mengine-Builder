from Builder.FileSystem import FileSystem
from Builder.TagHandler.TagHandler import TagHandler
from Builder.Operation.OperationManager import OperationManager
from Builder.Toolchain import converter_supported

class TagHandlerFragmentShader(TagHandler):
    def getFileNode(self):
        children = self.node.getChildren()
        for child in children:
            tagName = child.getTagName()
            if tagName == "File":
                return child
                pass
            pass
        pass

    def _onExecute(self):
        fileNode = self.getFileNode()

        if fileNode is None:
            return True
            pass

        Converter = fileNode.getAttribute("Converter")
        Path = fileNode.getAttribute("Path")

        if converter_supported(Converter) is False:
            self.node.removeFromParent()
            self.setDocumentToRewrite()
            return True

        if fileNode.hasAttribute("Converter"):
            fileNode.removeAttribute("Converter")
            pass

        SourcePath = self.fileSystemCursor.getFileSourcePath(Path)

        success = True

        if Converter is None or Converter == "":
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(Path)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("CopyFile", SourcePath=SourcePath, DestinationPath=DestinationPath, Doc="TagHandlerFragmentShader")
                pass

            success = oc.isSuccess()
        elif Converter == "text2pso":
            NewPath = FileSystem.setFileExtension(Path, "pso")
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(NewPath)
            fileNode.setAttribute("Path", NewPath)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertText2PSO", SourcePath=SourcePath, DestinationPath=DestinationPath)
                pass

            success = oc.isSuccess()
            pass
        elif Converter == "text2pso11":
            NewPath = FileSystem.setFileExtension(Path, "pso")
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(NewPath)
            fileNode.setAttribute("Path", NewPath)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertText2PSO11", SourcePath=SourcePath, DestinationPath=DestinationPath)
                pass

            success = oc.isSuccess()
            pass
        elif Converter == "text2metallib":
            NewPath = FileSystem.setFileExtension(Path, "metallib")
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(NewPath)
            fileNode.setAttribute("Path", NewPath)
            fileNode.setAttribute("Compile", "1")

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertText2Metallib", SourcePath=SourcePath, DestinationPath=DestinationPath)
                pass

            success = oc.isSuccess()
            pass
        pass

        self.setDocumentToRewrite()

        return success
        pass
    pass
