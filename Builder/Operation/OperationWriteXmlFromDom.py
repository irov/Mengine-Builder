from Builder.Operation.Operation import Operation
from Builder.FileSystem import FileSystem

class OperationWriteXmlFromDom(Operation):
    def _onParams( self, params ):
        self.rootElement = params.pop("RootDomElement")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return "destination  %s"%(self.destinationPath)
        pass

    def _onRun(self):
        root = self.rootElement.cloneNode(deep=True)
        for node in [root] + list(root.getElementsByTagName("*")):
            if node.hasAttribute("__Dir"):
                node.removeAttribute("__Dir")
        xml = root.toprettyxml(encoding='UTF-8', indent="  ", newl="\n")
        FileSystem.filePutContents(self.destinationPath, xml)

        return True
        pass
    pass
