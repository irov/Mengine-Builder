from Builder.TagHandler.ResourceHandler.ResourceHandlerMusicConvert import ResourceHandlerMusicConvert

class ResourceHandlerMusicConvertToAAC(ResourceHandlerMusicConvert):
    def _workWithFileNode(self, fileNode):
        self.convertFFMPEG(fileNode, "aac", "ConvertFFMPEGtoAAC", "aacSound")

        return True
        pass
    pass
