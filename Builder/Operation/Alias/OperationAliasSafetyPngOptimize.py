from Builder.Operation.Operation import Operation
from Builder.Operation.OperationManager import OperationManager

class OperationAliasSafetyPngOptimize(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.premultiply = params.pop("Premultiply", self.project.imagePremultiply is True)
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath  ) )
        pass

    def _onRun(self):
        with OperationManager.runOperationChain() as oc:
            oc.addOperation("PngOptimize", SourcePath=self.sourcePath, DestinationPath=self.destinationPath,
                            Premultiply=self.premultiply)
            pass

        return oc.isSuccess()
        pass
    pass
