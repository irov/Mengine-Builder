from Builder.Error.ErrorHandler import ErrorHandler

from Builder.TagHandler.TagHandler import TagHandler

class TagHandlerResource(TagHandler):
    def __init__(self, resourceHandlerPool):
        super(TagHandler, self).__init__()
        self.resourceHandlerPool = resourceHandlerPool
        self.scanChildren = True
        pass

    def onParams(self, pakName, node, parserContext, pool):
        super(TagHandlerResource, self).onParams(pakName, node, parserContext, pool)
        self.scanChildren = True
        pass

    def needToScanChildren(self):
        return self.scanChildren

    def _onExecute(self):
        if self.node.hasAttribute("Skip") is True:
            return True
            pass

        if self.node.hasAttribute("Type") is False:
            return True
            pass

        type = self.node.getAttribute("Type")
        if type in ("ResourceScene", "ResourceMotion"):
            self.scanChildren = False
            pass
        handler = self.resourceHandlerPool.getHandler(type)

        if handler is None:
            return True
            pass

        pool = self.parserContext.getTagHandlerPool()

        handler.onParams(self.pakName, self.node, self.parserContext, pool)

        if handler.execute() is False:
            ErrorHandler.warning("invalid execute [%s] pak [%s]", self.__repr__(), self.pakName)
            return False

        return True
        pass
    pass
