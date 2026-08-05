from PyBuilder.Operation.Operation import Operation
from PyBuilder.FileSystem import FileSystem

class OperationWriteXmlFromDom(Operation):
    def _onParams( self, params ):
        self.rootElement = params.pop("RootDomElement")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return "destination  %s"%(self.destinationPath)
        pass

    def _onRun(self):
        xml = self.rootElement.toprettyxml(encoding='UTF-8', indent="  ", newl="\n")
        FileSystem.filePutContents(self.destinationPath, xml)

        return True
        pass
    pass
