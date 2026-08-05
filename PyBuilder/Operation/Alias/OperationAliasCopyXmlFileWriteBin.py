from PyBuilder.Operation.Operation import Operation
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.OperationManager import OperationManager

from PyBuilder.Constants import XML_2_BIN_DLL_PATH,BIN_EXTENSION
from PyBuilder.Environment import Environment

class OperationAliasCopyXmlFileWriteBin(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath  ) )
        pass

    def _onRun(self):
        project = Environment.getCurrentProject()
        protocolPath = project.pathToProtocolXml

        destination = FileSystem.setFileExtension(self.destinationPath, BIN_EXTENSION)
        with OperationManager.runOperationChain() as oc:
            oc.addOperation("ConvertXmlToBin", SourcePath = self.sourcePath, DestinationPath = destination
                            ,ProtocolPath = protocolPath, Xml2BinDllName = XML_2_BIN_DLL_PATH)
            pass

        return oc.isSuccess()
        pass
    pass
