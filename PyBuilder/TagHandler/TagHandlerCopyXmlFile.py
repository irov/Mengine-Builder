__author__ = 'human88998999877'
from PyBuilder.TagHandler.TagHandler import TagHandler
from PyBuilder.Operation.OperationManager import OperationManager

class TagHandlerCopyXmlFile(TagHandler):
    def copyXmlFile(self, sourcePath, destinationPath):
        sourceFull = self.fileSystemCursor.getFileSourcePath(sourcePath)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destinationPath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation( 'CopyXmlFile', SourcePath = sourceFull, DestinationPath = destinationFull )
            pass
        pass
    pass
