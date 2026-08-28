from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem

class OperationRenameFile(Operation):
    def _onParams( self, params ):
        self.oldName = params.pop("OldName")
        self.newName = params.pop("NewName")
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.oldName, self.newName  ) )
        pass

    def _onRun(self):
        FileSystem.renameFile(self.oldName,self.newName)

        return True
        pass
    pass
