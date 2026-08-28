__author__ = 'human88998999877'
class GraphRootContext(object):
    def __init__(self, fileSystemCursor, document, tagHandlerPool):
        self.fileSystemCursor = fileSystemCursor
        self.document = document
        self.pool = tagHandlerPool
        pass

    def getTagHandlerPool(self):
        return self.pool
        pass

    def getFileSystemCursor(self):
        return self.fileSystemCursor
        pass

    def getDocument(self):
        return self.document
        pass
    pass
