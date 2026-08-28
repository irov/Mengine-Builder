from Builder.Error.ErrorHandler import ErrorHandler

from Builder.TagHandler.TagHandlerFile import TagHandlerFile

from Builder.Operation.OperationManager import OperationManager

class TagHandlerFont(TagHandlerFile):
    def _onExecute(self):
        if self.node.hasAttribute("Path") is False:
            ErrorHandler.warning("not set Path [%s]", self.__repr__())
            return False
            pass

        Path = self.node.getAttribute("Path")

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyFonts", Path=Path, fileSystemCursor=self.fileSystemCursor)
            pass

        return oc.isSuccess()
        pass
    pass
