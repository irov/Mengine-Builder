from Builder.Operation.Operation import Operation
from Builder import Compile


class OperationValidatePyFile(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")

    def _getInfo(self):
        return "source %s" % self.sourcePath

    def _onRun(self):
        return Compile.validate_python(self.sourcePath)
