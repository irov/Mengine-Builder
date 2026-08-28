from Builder.Error.ErrorHandler import ErrorHandler

from Builder.TagHandler.TagHandler import TagHandler

class TagHandlerResource(TagHandler):
    def __init__(self, resourceHandlerPool):
        super(TagHandler, self).__init__()
        self.resourceHandlerPool = resourceHandlerPool
        pass

    def _onExecute(self):
        if self.node.hasAttribute("Skip") is True:
            return True
            pass

        if self.node.hasAttribute("Type") is False:
            return True
            pass

        type = self.node.getAttribute("Type")
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
