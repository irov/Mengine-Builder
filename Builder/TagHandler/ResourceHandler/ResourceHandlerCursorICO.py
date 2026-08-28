from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler

class ResourceHandlerCursorICO(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def _workWithFileNode(self, fileNode):
        filename = fileNode.getAttribute("Path")

        if fileNode.hasAttribute("__Dir"):
            sourceFull = fileNode.getAttribute("__Dir")
            pass
        else:
            sourceFull = self.fileSystemCursor.getFileSourcePath(filename)
            pass

        destinationFull = self.fileSystemCursor.getFileDestinationPath(filename)

        self.copyFile(sourceFull, destinationFull)

        return True
        pass
    pass
