from Builder.TagHandler.ResourceHandler.ResourceHandlerMusicConvert import ResourceHandlerMusicConvert

class ResourceHandlerMusicConvertToMP3(ResourceHandlerMusicConvert):
    def _workWithFileNode(self, fileNode):
        self.convertFFMPEG(fileNode, "mp3", "ConvertFFMPEGtoMP3", "mp3Sound")

        return True
        pass
    pass
