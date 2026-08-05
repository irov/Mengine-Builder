from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.FileSystem import FileSystem

class TagHandlerScripts(TagHandler):
    def _onExecute(self):
        nodes = self.node.getChildrenByTag("Script")

        if len(nodes) == 0:
            nodes = [self.node]
            pass

        for node in nodes:
            Path = node.getAttribute("Path")
            fileSystemCursor = self.fileSystemCursor.getBranch(Path)

            sourceDir = fileSystemCursor.getSourceDir()
            destinationDir = fileSystemCursor.getDestinationDir()

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("CopyDirRecursive", SourcePath=sourceDir,
                               DestinationPath=destinationDir,
                               IgnoredPatterns=".svn", CopyFileCallback=self.onCopyFile)
                pass
            pass

        return True

    def needToScanChildren(self):
        return False

    def onCopyFile(self, fileSource, fileDestiny):
        if self.project.compilePython is True:
            extension = FileSystem.getFileExtension(fileSource)
            if extension == "py":
                fileDestiny_pyo = FileSystem.setFileExtension(fileDestiny, "pyo")
                fileDestiny_pyz = FileSystem.setFileExtension(fileDestiny, "pyz")
                with OperationManager.runOperationChain() as oc:
                    oc.addOperation("CopyFile", SourcePath=fileSource, DestinationPath=fileDestiny, Doc="TagHandlerScripts")
                    oc.addOperation("CompilePyFile", SourcePath=fileDestiny)
                    oc.addOperation("RemoveFile", SourcePath=fileDestiny)
                    oc.addOperation("CompressPyoFile", SourcePath=fileDestiny_pyo, DestinationPath=fileDestiny_pyz)
                    pass
                pass
            elif extension == "pyo" or extension == "pyc":
                #Don`t COPY
                return
                pass
            pass
        else:
            extension = FileSystem.getFileExtension(fileSource)
            if extension == "py":
                with OperationManager.runOperationChain() as oc:
                    oc.addOperation("CopyFile", SourcePath=fileSource, DestinationPath=fileDestiny, Doc="TagHandlerScripts")
                    pass
                pass
            pass
        pass
    pass
