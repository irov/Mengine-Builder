from Builder.TagHandler.TagHandlerFile import TagHandlerFile

class TagHandlerOutlineImage(TagHandlerFile):
    def _onExecute(self):
        if self.node.hasAttribute("Path"):
            path = self.node.getAttribute("Path")
            self.copyFile(path,path)

        return True
        pass
    pass
