from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler

class OperationPngOptimize(Operation):
    def _getInfo(self):
        return "AlphaSpreading image %s" % self.sourcePath
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.premultiply = params.pop("Premultiply", self.project.imagePremultiply is True)
        pass

    def _onRun(self):
        return self.project.pngOptimizer.optimize(self.sourcePath, self.destinationPath, self.premultiply)
        pass
    pass
