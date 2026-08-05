from PyBuilder.FileSystem import FileSystem
from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Error.ErrorHandler import ErrorHandler

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
        filename = FileSystem.setFileExtension(path, "xml")

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

        return True
        pass

    def _onFinalise(self):
        TagHandler.includes.pop()

        if self.collector is not None:
            self.collector.unlockSection()
            pass
        pass
    pass
