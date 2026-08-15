__author__ = 'human88998999877'
from PyBuilder.Error.ErrorHandler import  ErrorHandler

class GraphRoot:
    def __init__(self, pakName, sourceRelativeFilePath, fileSystemCursor, metabufNode="DataBlock"):
        self.pakName = pakName
        self.sourceRelativeFilePath = sourceRelativeFilePath
        self.fileSystemCursor = fileSystemCursor
        self.metabufNode = metabufNode
        self.children = {}
        self._isRewrite = False
        pass

    def __repr__(self):
        className = str(self.__class__)
        return "GraphDocument %s  on   %s - %s" % (className,self.fileSystemCursor, self.sourceRelativeFilePath)
        pass

    def hasChild(self, path):
        if path in self.children:
            return True
            pass

        return False
        pass

    def getChild(self, path):
        if self.hasChild(path) is False:
            child = self._createChild(path)
            self.children[path] = child
            pass

        return self.children[path]
        pass

    def initialise(self):
        if self._onInitialise() is False:
            ErrorHandler.warning(" Parser initialise`s failure on  %s", self.__repr__())
            return False
            pass

        return True
        pass

    def visit(self, tagHandlerPool):
        if self._onVisit(tagHandlerPool) is False:
            ErrorHandler.warning(" GraphDocument visit`s failure on [%s]", self.__repr__())
            return False
            pass

        return True
        pass

    def finalise(self):
        for path, child in self.children.items():
            if child.finalise() is False:
                ErrorHandler.warning("invalid finalize graph root [%s] [%s]" % (self.__repr__(), child))

                return False
                pass
            pass

        if self._onFinalise() is False:
            ErrorHandler.warning("Parser finalise`s failure on [%s]", self.__repr__())

            return False
            pass

        return True
        pass

    def setRewrite(self):
        self._isRewrite = True
        pass

    def isRewrite(self):
        return self._isRewrite
        pass

    def _onVisit(self, tagHandlerPool):
        raise BaseException("Abstract")
        pass

    def _createChild(self, path):
        raise BaseException("Abstract")
        pass

    def _onFinalise(self):
        raise BaseException("Abstract")
        pass

    def _onInitialise(self):
        raise BaseException("Abstract")
        pass
    pass
