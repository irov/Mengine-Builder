from Builder import Tools

from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem


class OperationConvertMetabuf(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.inputFormat = params.pop("InputFormat")
        self.meta = params.pop("Meta", "Data")
        self.node = params.pop("Node")

    def _getInfo(self):
        return "source %s destination %s format %s node %s" % (
            self.sourcePath,
            self.destinationPath,
            self.inputFormat,
            self.node,
        )

    def _onRun(self):
        if FileSystem.isFile(self.sourcePath) is False:
            ErrorHandler.warning("Operation %s failed: file %s does not exist", self, self.sourcePath)
            return False

        if self.inputFormat not in ("json", "xml"):
            ErrorHandler.warning("Operation %s failed: unsupported input format %s", self, self.inputFormat)
            return False

        directory = FileSystem.getDirname(self.destinationPath)

        if directory != "" and FileSystem.isDirectory(directory) is False:
            FileSystem.makeDirsRecursive(directory)

        if Tools.writeBin(
            self.inputFormat,
            self.meta,
            self.node,
            self.sourcePath,
            self.destinationPath,
        ) is False:
            ErrorHandler.warning(
                "invalid Metabuf conversion [%s] source [%s] destination [%s]",
                self.__repr__(),
                self.sourcePath,
                self.destinationPath,
            )
            return False

        return True
