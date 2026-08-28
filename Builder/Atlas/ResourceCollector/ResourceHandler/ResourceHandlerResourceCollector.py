from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler

from Builder.Error.ErrorHandler import ErrorHandler

class ResourceHandlerResourceCollector(ResourceHandler):
    def __init__(self, collector, resourceClass):
        super(ResourceHandlerResourceCollector, self).__init__()
        self.collector = collector
        self.resourceClass = resourceClass
        pass

    def _onExecute(self):
        resource = self.resourceClass()
        if resource.initialise(self.node, self.collector, self.fileSystemCursor, self.pool, self.includes) is False:
            ErrorHandler.warning("invalid initialize resource class [%s]", self.__repr__())

            return False
            pass

        self.setDocumentToRewrite()

        return True
        pass
    pass
