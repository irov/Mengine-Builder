from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
from Builder.Graph.GraphNodeJson import GraphNodeJson
from Builder.Graph.GraphRoot import GraphRoot
from Builder.Graph.GraphRootContext import GraphRootContext
from Builder.Graph.GraphRootXmlDom import GraphRootXmlDom
from Builder.Operation.OperationManager import OperationManager
from Builder.Environment import Environment


class GraphRootJson(GraphRoot):
    def _onInitialise(self):
        pathToJson = self.fileSystemCursor.getFileSourcePath(self.sourceRelativeFilePath)
        self.documentJson = FileSystem.jsonFileLoadContents(pathToJson)

        if isinstance(self.documentJson, dict) is False:
            ErrorHandler.warning("invalid JSON package document %s" % pathToJson)
            return False

        return True

    def _createChild(self, path):
        branch = self.fileSystemCursor.getBranch("")

        if FileSystem.getFileExtension(path) == "json":
            child = GraphRootJson(self.pakName, path, branch)
        else:
            child = GraphRootXmlDom(self.pakName, path, branch)

        if child.initialise() is False:
            return None

        return child

    def _onVisit(self, tagHandlerPool):
        rootNode = GraphNodeJson(None, self.documentJson)

        if self.walk(rootNode, tagHandlerPool) is False:
            ErrorHandler.warning("invalid walk [%s] [%s]" % (self.__repr__(), rootNode))
            return False

        return True

    def walk(self, root, tagHandlerPool):
        for node in root.getChildren():
            tagName = node.getTagName()
            fileSystemCursor = self.fileSystemCursor.getBranch("")
            context = GraphRootContext(fileSystemCursor, self, tagHandlerPool)
            handler = tagHandlerPool.getHandler(tagName)

            if handler is not None:
                handler.onParams(self.pakName, node, context, tagHandlerPool)

                if handler.execute() is False:
                    ErrorHandler.warning("invalid execute %s [%s] [%s]" % (tagName, self.__repr__(), handler))
                    return False

                if handler.needToScanChildren() is True:
                    if self.walk(node, tagHandlerPool) is False:
                        ErrorHandler.warning("invalid walk %s [%s] [%s]" % (tagName, self.__repr__(), handler))
                        return False
                    pass

                handler.finalise()
                pass
            else:
                if tagName not in GraphRootXmlDom.unknownTags:
                    GraphRootXmlDom.unknownTags[tagName] = 0
                    pass

                GraphRootXmlDom.unknownTags[tagName] += 1

                if self.walk(node, tagHandlerPool) is False:
                    ErrorHandler.warning("invalid walk [%s] [%s]" % (self.__repr__(), node))
                    return False
                pass
            pass

        return True

    def _onFinalise(self):
        destination = self.fileSystemCursor.getFileDestinationPath(self.sourceRelativeFilePath)
        source = self.fileSystemCursor.getFileSourcePath(self.sourceRelativeFilePath)
        project = Environment.getCurrentProject()

        if project.isMetabuf is True:
            if self.isRewrite() is True:
                directory = FileSystem.getDirname(self.sourceRelativeFilePath)
                tempRoot = project.logDir if project.logDir is not None else project.destinationDir
                tempDirectory = FileSystem.joinAndNormalisePath(tempRoot, "metabuf" if directory == "" else "metabuf/%s" % directory)
                FileSystem.makeDirsRecursiveIfNotExist(tempDirectory)
                source = FileSystem.joinAndNormalisePath(tempDirectory, FileSystem.getBasename(self.sourceRelativeFilePath))
                FileSystem.jsonFileDumpContent(source, self.documentJson)

            destination = FileSystem.setFileExtension(destination, "bin")

            with OperationManager.runOperationChain() as oc:
                oc.addOperation(
                    "ConvertMetabuf",
                    SourcePath=source,
                    DestinationPath=destination,
                    InputFormat="json",
                    Meta="Data",
                    Node=self.metabufNode,
                )

            return oc.isSuccess()

        if self.isRewrite() is True:
            destinationDir = FileSystem.getDirname(destination)
            FileSystem.makeDirsRecursiveIfNotExist(destinationDir)
            FileSystem.jsonFileDumpContent(destination, self.documentJson)
            return True

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyFile", SourcePath=source, DestinationPath=destination, Doc="GraphRootJson")
            pass

        return oc.isSuccess()
    pass
