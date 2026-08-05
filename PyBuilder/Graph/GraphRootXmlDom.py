from xml.dom.minidom import  parse
import xml.parsers.expat

from PyBuilder.Constants import BIN_EXTENSION
from PyBuilder.Error.ErrorHandler import  ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Graph.GraphRootContext import GraphRootContext
from PyBuilder.Graph.GraphRoot import GraphRoot
from PyBuilder.Graph.GraphNodeXmlDom import GraphNodeXmlDom

class GraphRootXmlDom(GraphRoot):
    unknownTags = {}

    @staticmethod
    def getUnknownTags():
        return GraphRootXmlDom.unknownTags
        pass

    def _onInitialise(self):
        pathToXml = self.fileSystemCursor.getFileSourcePath(self.sourceRelativeFilePath)

        self.documentXmlDom = self.openDocument(pathToXml)

        if self.documentXmlDom is None:
            return False
            pass

        return True
        pass

    def openDocument(self, pathToXml):
        document = None

        try:
            document = parse(pathToXml)
            pass
        except IOError as e:
            message = "Parser.parseToDom IOError %s in %s " % ( str(e) ,self )
            ErrorHandler.warning(message)
            return None
            pass
        except xml.parsers.expat.ExpatError as e:
            message = "Parser.parseToDom xml.parsers.expat.ExpatError %s in %s " % (str(e) , self )
            ErrorHandler.warning(message)
            return None
            pass

        return document
        pass

    def _createChild(self, path):
        branch = self.fileSystemCursor.getBranch("")
        child = GraphRootXmlDom(self.pakName, path, branch)

        if child.initialise() is False:
            return None
            pass

        return child
        pass

    def _onVisit(self, tagHandlerPool):
        rootNode = GraphNodeXmlDom(self.documentXmlDom)
        if self.walk(rootNode, tagHandlerPool) is False:
            ErrorHandler.warning("invalid walk [%s] [%s]", self.__repr__(), rootNode)
            return False

        return True
        pass

    def walk(self, root, tagHandlerPool):
        for node in root.getChildren():
            tagName = node.getTagName()
            #dom = node.getXmlDomElement()
            #print("walk",tagName,dom)

            fileSystemCursor = self.fileSystemCursor.getBranch("")
            context = GraphRootContext(fileSystemCursor, self, tagHandlerPool)

            handler = tagHandlerPool.getHandler(tagName)

            if handler is not None:
                handler.onParams(self.pakName, node, context, tagHandlerPool)
                if handler.execute() is False:
                    ErrorHandler.warning("invalid execute %s [%s] [%s]", tagName, self.__repr__(), handler)
                    return False

                if handler.needToScanChildren() is True:
                    if self.walk(node, tagHandlerPool) is False:
                        ErrorHandler.warning("invalid walk %s [%s] [%s]", tagName, self.__repr__(), handler)
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
                    ErrorHandler.warning("invalid walk [%s] [%s]", self.__repr__(), node)
                    return False
                pass
            pass

        return True
        pass

    def _onFinalise(self):
        if self.isRewrite() is True:
            self.rewriteXmlFromDom()
            pass
        else:
            self.copyXml()
            pass

        return True
        pass

    def rewriteXmlFromDom(self):
        destination = self.fileSystemCursor.getFileDestinationPath(self.sourceRelativeFilePath)
        source = self.fileSystemCursor.getFileSourcePath(self.sourceRelativeFilePath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('AliasRewriteXmlFromXmlDomDocument'
                            , SourcePath = source
                            , DestinationPath = destination
                            , RelativeFilePath = self.sourceRelativeFilePath
                            , Document = self.documentXmlDom )
            pass
        pass

    def copyXml(self):
        #targetRelativePath = FileSystem.setFileExtension(self.sourceRelativeFilePath, BIN_EXTENSION)
        destination = self.fileSystemCursor.getFileDestinationPath(self.sourceRelativeFilePath)
        source = self.fileSystemCursor.getFileSourcePath(self.sourceRelativeFilePath)

        with OperationManager.runOperationChain() as oc:
            oc.addOperation( 'CopyXmlFile', SourcePath = source, DestinationPath = destination )
            pass
        pass

    def getRootNode(self):
        rootElement = GraphNodeXmlDom(self.documentXmlDom.documentElement)
        return rootElement
        pass
    pass
"""
    def createNode(self, xmlDomNode):
        return GraphNodeXmlDom(xmlDomNode)
        pass
"""
#    def getBaseAndTargetFilesForXmlFile(self):
#        applicationNode = self.applicationDescription
#
#        filename = FileSystem.getBasename(self.nodeDescription.pathToXml)
#        sourceDirName =   FileSystem.getDirname(self.nodeDescription.pathToXml)
#        sourceDirName = FileSystem.normalisePath(sourceDirName)
#
#        targetDirChain = sourceDirName.replace(applicationNode.baseDir, "" )
#        if targetDirChain[0] == "\\":
#            targetDirChain = targetDirChain[1:len(targetDirChain)]
#
#        targetDirName = FileSystem.joinPath(applicationNode.targetDir,targetDirChain)
#
#        baseFile = FileSystem.joinAndNormalisePath (sourceDirName , filename)
#        targetFile = FileSystem.joinAndNormalisePath (targetDirName , filename)
#        return (baseFile,targetFile)
#        pass
