from PyBuilder.Operation.Operation import Operation
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Environment import Environment
from PyBuilder.FileSystem import FileSystem

class OperationAliasRewriteXmlFromXmlDomDocument(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.relativeFilePath = params.pop("RelativeFilePath")
        self.document = params.pop("Document")
        pass

    def _getInfo(self):
        return ("source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath  ) )
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.relativeFilePath)
        fileName = FileSystem.getBasename(self.sourcePath)
        project = Environment.getCurrentProject()
        logDir = project.logDir
        tempDir = FileSystem.joinAndNormalisePath(logDir, "xml" if len(dirName) == 0 else "xml/%s"%(dirName))
        FileSystem.makeDirsRecursiveIfNotExist(tempDir)
        tempPath = FileSystem.joinAndNormalisePath(tempDir, fileName)

        #targetRelativePath = FileSystem.setFileExtension(self.sourceRelativeFilePath, BIN_EXTENSION)
        with OperationManager.runOperationChain() as oc:
            oc.addOperation("WriteXmlFromDom", RootDomElement = self.document.documentElement, DestinationPath = tempPath)
            oc.addOperation("CopyXmlFile", SourcePath = tempPath, DestinationPath = self.destinationPath)
            # oc.addOperation("RemoveFile", SourcePath = tempPath)
            pass

        return oc.isSuccess()
        pass
    pass
