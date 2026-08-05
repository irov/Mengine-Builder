__author__ = 'human88998999877'

from PyBuilder.Error.ErrorHandler import ErrorHandler

class Resource(object):
    def __init__(self):
        super(Resource, self).__init__()
        self.collector = None
        self.node = None
        self.pool = None
        pass

    def __repr__(self):
        return "%s :: name %s type %s %s "%(self.__class__.__name__, self.node.getAttribute("Name"),self.node.getAttribute("Name"),hex(id(self)))
        pass

    def initialise(self, node, collector, fileSystemCursor, pool, includes):
        self.node = node
        self.collector = collector
        self.fileSystemCursor = fileSystemCursor
        self.pool = pool
        self.includes = includes

        if self._onSkip() is True:
            return True
            pass

        if self._onInitialise() is False:
            ErrorHandler.warning("invalid initialize resource [%s]", self.__repr__())

            return False
            pass

        self.collector.addResource(self.getName(), self)

        return True
        pass

    def getType(self):
        return self.node.getAttribute("Type")
        pass

    def getName(self):
        return self.node.getAttribute("Name")
        pass

    def getFileSystemCursor(self):
        return self.fileSystemCursor
        pass

    def _onSkip(self):
        return False
        pass

    def _onInitialise(self):
        return True
        pass

    def isSkip(self):
        return self.node.getAttribute("Skip")
        pass

    def setSkip(self):
        self.node.setAttribute("Skip", "1")
        pass

    def setAlreadyInAtlas(self):
        self.node.setAttribute("AlreadyInAtlas", "1")
        pass

    def isAlreadyInAtlas(self):
        return self.node.getAttribute("AlreadyInAtlas")
        pass
    pass
