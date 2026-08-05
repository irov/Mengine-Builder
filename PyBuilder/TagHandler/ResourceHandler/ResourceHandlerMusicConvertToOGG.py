from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerMusicConvert import ResourceHandlerMusicConvert

class ResourceHandlerMusicConvertToOGG(ResourceHandlerMusicConvert):
    def _workWithFileNode(self, fileNode):
        self.convertFFMPEG(fileNode, "ogg", "ConvertFFMPEGtoOGG", "oggSound", Quality=self.project.musicConvertQuality)

        return True
        pass
    pass
