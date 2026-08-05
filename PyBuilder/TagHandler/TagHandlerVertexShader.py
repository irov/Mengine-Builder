from PyBuilder.FileSystem import FileSystem
from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Toolchain import converter_supported

class TagHandlerVertexShader(TagHandler):
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
                oc.addOperation("CopyFile", SourcePath=SourcePath, DestinationPath=DestinationPath, Doc="TagHandlerVertexShader")
                pass

            success = oc.isSuccess()
        elif Converter == "text2vso":
            NewPath = FileSystem.setFileExtension(Path, "vso")
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(NewPath)

            fileNode.setAttribute("Path", NewPath)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertText2VSO", SourcePath=SourcePath, DestinationPath=DestinationPath)
                pass

            success = oc.isSuccess()
            pass
        elif Converter == "text2vso11":
            NewPath = FileSystem.setFileExtension(Path, "vso")
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(NewPath)

            fileNode.setAttribute("Path", NewPath)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertText2VSO11", SourcePath=SourcePath, DestinationPath=DestinationPath)
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
        elif Converter == "vsc":
            DestinationPath = self.fileSystemCursor.getFileDestinationPath(Path)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("CopyFile", SourcePath=SourcePath, DestinationPath=DestinationPath, Doc="TagHandlerVertexShader vsc")
                pass

            success = oc.isSuccess()
            pass

        self.setDocumentToRewrite()

        return success
        pass
    pass
