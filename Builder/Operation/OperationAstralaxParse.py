from Builder.Operation.Operation import Operation
from Builder.FileSystem import FileSystem

from Builder.Operation.OperationManager import OperationManager

from Builder import Tools

class OperationAstralaxParse(Operation):
    def _getInfo(self):
        return "source  %s \n\r destiny %s" % ( self.sourcePath, self.destinationPath )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _onRun(self):
        sourceDirName = FileSystem.getDirname(self.sourcePath)
        atlasFiles = Tools.magicParticlesAtlasFiles(self.sourcePath)

        if atlasFiles is None:
            return False
            pass

        with OperationManager.runOperationChain() as oc:
            for atlasFile in atlasFiles:
                sourceNew = FileSystem.joinAndNormalisePath(sourceDirName, atlasFile)
                destinationNew = FileSystem.joinAndNormalisePath(self.destinationPath, atlasFile)
                oc.addOperation("CopyFile", SourcePath = sourceNew, DestinationPath = destinationNew, Doc="OperationAstralaxParse")
                pass
            pass

        return oc.isSuccess()
        pass
    pass
