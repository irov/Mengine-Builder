import ToolsBuilderPlugin

from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem

class OperationConvertXmlToBin(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.protocolPath = params.pop("ProtocolPath")
        self.dllName = params.pop("Xml2BinDllName")
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath))
        pass

    def _onRun(self):
        if  not FileSystem.isFile(self.sourcePath):
            ErrorHandler.warning("Operation %s failed  File %s not exist", self, self.sourcePath)
            return False
            pass

        dirName = FileSystem.getDirname(self.destinationPath)

        if FileSystem.isDirectory(dirName) == False and dirName != '':
            FileSystem.makeDirsRecursive(dirName)
            pass

        if ToolsBuilderPlugin.writeBin(self.protocolPath, self.sourcePath, self.destinationPath) is False:
            ErrorHandler.warning("invalid write bin [%s] protocol [%s] source [%s] destination [%s]", self.__repr__(),
                                 self.protocolPath, self.sourcePath, self.destinationPath)
            return False
            pass

        return True
        pass
    pass
