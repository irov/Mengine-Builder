from PyBuilder.Graph.GraphFileSystemCursor import GraphFileSystemCursor
from PyBuilder.Graph.GraphRootJson import GraphRootJson
from PyBuilder.Graph.GraphRootXmlDom import GraphRootXmlDom
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem

class ResourcePack(object):
    def __init__(self, project, name, relativePathToDescription, exportDir, sourceDir, destinationDir):
        self.project = project
        self.name = name
        self.rootFileSystemCursor = GraphFileSystemCursor(self.project, exportDir, sourceDir, destinationDir)
        self.exportDir = exportDir
        self.destinationDir = destinationDir
        self.sourceDir = sourceDir
        self.toZip = False
        self.pathToZip = None
        self.relativePathToDescription = relativePathToDescription
        self.rootDocument = None
        self.resources = {}
        pass

    def addResource(self, name, node):
        self.resources[name] = node
        pass

    def hasResource(self, name):
        return name in self.resources
        pass

    def getResource(self, name):
        return self.resources[name]
        pass

    def initialise(self):
        if self.rootFileSystemCursor.isValid() is False:
            ErrorHandler.error("ResourcePack initialise source directory %s not exist" % self.sourceDir)
            return False
            pass

        if self.relativePathToDescription is not None:
            extension = FileSystem.getFileExtension(self.relativePathToDescription)

            if extension == "json":
                self.rootDocument = GraphRootJson(self.name, self.relativePathToDescription, self.rootFileSystemCursor)
                pass
            else:
                self.rootDocument = GraphRootXmlDom(self.name, self.relativePathToDescription, self.rootFileSystemCursor)
                pass

            if self.rootDocument.initialise() is False:
                ErrorHandler.warning("invalid root document initialize")

                return False
                pass
            pass

        return True
        pass

    def setToZip(self, state):
        self.toZip = state
        pass

    def setPathToZip(self, pathToZip):
        self.pathToZip = pathToZip
        pass

    def isNeedToZip(self):
        return self.toZip
        pass

    def visit(self, tagHandlerPool):
        if self.rootDocument is not None:
            if self.rootDocument.visit(tagHandlerPool) is False:
                ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())

                return False
            pass
        else:
            with OperationManager.runOperationChain() as oc:
                oc.addOperation("CopyDirRecursive", SourcePath=self.sourceDir, DestinationPath=self.destinationDir)
                pass

            if oc.isSuccess() is False:
                return False
            pass

        return True
        pass

    def finalise(self):
        if self.rootDocument is not None:
            self.rootDocument.finalise()
            pass
        pass

    def convertDestinationToZip(self):
        ErrorHandler.importantMessage(" create zip pack from %s to %s " %(self.destinationDir, self.pathToZip))
        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CreateZipPack", SourcePath=self.destinationDir, DestinationPath=self.pathToZip, SplitSize=self.project.CreatePacksLimit)
            pass

        return oc.isSuccess()
        pass

    def removeDestination(self):
        with OperationManager.runOperationChain() as oc:
            oc.addOperation("RemoveDirRecursive", SourcePath=self.destinationDir)
            pass

        return oc.isSuccess()
        pass

    def getFileSystemCursor(self):
        return self.rootFileSystemCursor
        pass

    def getSourceDir(self):
        return self.sourceDir
        pass

    def getDestinationDir(self):
        return self.destinationDir
        pass

    def getPathToDescription(self):
        return self.pathToDescription
        pass
    pass
