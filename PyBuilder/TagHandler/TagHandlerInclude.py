from PyBuilder.FileSystem import FileSystem
from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Environment import Environment

class TagHandlerInclude(TagHandler):
    def __init__(self, collector = None):
        self.collector = collector
        pass

    def _onExecute(self):
        # children1 = self.node.getChildrenByTag("Include")
        # print(children1)
        if self.collector is not None:
            self.collector.lockSection()
            pass

        document = self.parserContext.getDocument()
        pool = self.parserContext.getTagHandlerPool()

        path = self.node.getAttribute("Path")
        extension = FileSystem.getFileExtension(path)

        if extension in ("json", "xml"):
            filename = path
        elif extension == "bin":
            jsonFilename = FileSystem.setFileExtension(path, "json")
            xmlFilename = FileSystem.setFileExtension(path, "xml")
            filename = jsonFilename if document.hasChild(jsonFilename) is True else xmlFilename
        else:
            ErrorHandler.error("include Path must explicitly use .json, .xml or .bin: %s" % path)
            return False

        childDocument = document.getChild(filename)

        if childDocument is None:
            ErrorHandler.error("can`t open resource file %s" % filename)
            return False
            pass

        TagHandler.includes.append(self.node)

        if childDocument.visit(pool) is False:
            ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())

            return False
            pass

        project = Environment.getCurrentProject()

        if project.isMetabuf is True and extension in ("json", "xml"):
            self.node.setAttribute("Path", FileSystem.setFileExtension(path, "bin"))
            self.setDocumentToRewrite()

        return True
        pass

    def _onFinalise(self):
        TagHandler.includes.pop()

        if self.collector is not None:
            self.collector.unlockSection()
            pass
        pass
    pass
