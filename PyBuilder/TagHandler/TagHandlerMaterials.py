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

            extension = FileSystem.getFileExtension(path)

            if extension in ("json", "xml"):
                filename = path
            elif extension == "bin":
                jsonFilename = FileSystem.setFileExtension(path, "json")
                xmlFilename = FileSystem.setFileExtension(path, "xml")
                filename = jsonFilename if document.hasChild(jsonFilename) is True else xmlFilename
            else:
                ErrorHandler.error("material Path must explicitly use .json, .xml or .bin: %s" % path)
                return False

            childDocument = document.getChild(filename)

            if childDocument is None:
                ErrorHandler.error("can`t open resource file %s" % filename)

                return False
                pass

            if childDocument.visit(pool) is False:
                ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())

                return False
                pass

            project = Environment.getCurrentProject()

            if project.isMetabuf is True and extension in ("json", "xml"):
                child.setAttribute("Path", FileSystem.setFileExtension(path, "bin"))
                self.setDocumentToRewrite()
            pass

        return True
        pass
    pass
