from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
#from PyBuilder.Atlas.AtlasMaker import AtlasMaker

class ResourceHandlerMovieCreateAtlas(ResourceHandler):
    def _onExecute(self):
        raise BaseException("SET IN IN SETUP if atlasMode != CREATE_ATLAS_FOR_MOVIE:")
#TODO ATLASSES !!!!!!!!!!!
#PIECE OF OLD CODE
#            nodeName = self.node.getAttribute("Name")
#            datablock = self.node.parentNode
#            if datablock.tagName != "DataBlock":
#                return
#                pass
#
#            document = self.node.parentNode.parentNode
#            maker = AtlasMaker()
#            isRewrite = maker.createAtlasForNodeImageResources(datablock, document, self.nodeDescription.baseDir, nodeName)
#            if isRewrite == False:
#                return
#                pass
#
#            self.nodeDescription.buildNodeDescription.setToRewrited(True)
        return True
        pass
    pass
