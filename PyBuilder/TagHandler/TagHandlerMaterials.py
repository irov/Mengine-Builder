from PyBuilder.FileSystem import FileSystem
from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Environment import Environment

class TagHandlerMaterials(TagHandler):
    def isEnableToExport(self):
        if self.node.hasAttribute("Tag") is False:
            return True
            pass

        project = Environment.getCurrentProject()

        if len(project.resourceTag) == 0:
            return False
            pass

        tag = self.node.getAttribute("Tag")

        if tag not in project.resourceTag:
            ErrorHandler.message("Resources export disable because resources export tag %s specified" % project.resourceTag)
            return False
            pass

        return True
        pass

    def _onExecute(self):
        if self.isEnableToExport() is False:
            self.node.removeFromParent()

            self.setDocumentToRewrite()
            return True
            pass

        children = self.node.getChildrenByTag("Material")
        document = self.parserContext.getDocument()
        pool = self.parserContext.getTagHandlerPool()

        for child in children:
            path = child.getAttribute("Path")

            if FileSystem.getFileExtension(path) == "json":
                filename = path
            else:
                filename = FileSystem.setFileExtension(path, "xml")

            childDocument = document.getChild(filename)

            if childDocument is None:
                ErrorHandler.error("can`t open resource file %s" % filename)

                return False
                pass

            if childDocument.visit(pool) is False:
                ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())

                return False
                pass
            pass

        return True
        pass
    pass
