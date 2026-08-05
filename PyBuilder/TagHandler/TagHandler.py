from PyBuilder.Error.ErrorHandler import ErrorHandler

from PyBuilder.Watcher.Watcher import Watcher

class TagHandler(object):
    includes = []

    def onParams(self, pakName, node, parserContext, pool):
        self.pakName = pakName
        self.node = node
        self.parserContext = parserContext
        self.pool = pool
        self.fileSystemCursor = self.parserContext.getFileSystemCursor()
        self.includes = TagHandler.includes[:]
        pass

    def setProject(self, project):
        self.project = project
        pass

    def report(self):
        pass

    def setDocumentToRewrite(self):
        document = self.parserContext.getDocument()
        document.setRewrite()
        pass

    def execute(self):
        self.report()
        interval_name = "Execute [{}]".format(self.__class__.__name__)
        Watcher.startInterval(interval_name)

        try:
            return self._onExecute()
        except Exception as e:
            ErrorHandler.error("TagHandler %s execute error %s" % (self.__class__.__name__, str(e)))
            return False
        finally:
            Watcher.stopInterval(interval_name)

    def needToScanChildren(self):
        return True
        pass

    def _onExecute(self):
        return True
        pass

    def finalise(self):
        return self._onFinalise()
        pass

    def _onFinalise(self):
        pass
    pass
