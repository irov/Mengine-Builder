from Builder.TagHandler.TagHandlerFile import TagHandlerFile

class TagHandlerImage(TagHandlerFile):
    def _onExecute(self):
        if self.node.hasAttribute("Path"):
            path = self.node.getAttribute("Path")
            self.copyFile(path,path)

        return True
        pass
    pass
