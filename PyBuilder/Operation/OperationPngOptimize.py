from PyBuilder.Operation.Operation import Operation
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.PngOptimizer import PngOptimizer

class OperationPngOptimize(Operation):
    def _getInfo(self):
        return ("image %s  optimized by hge pngopt " % (self.sourcePath ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _onRun(self):
        PngOptimizer.optimize(self.sourcePath, self.destinationPath)

        return True
        pass
    pass
