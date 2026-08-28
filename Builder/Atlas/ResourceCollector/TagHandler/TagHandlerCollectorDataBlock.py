from Builder.TagHandler.TagHandler import TagHandler

from Builder.Constants import ATLAS_NAME_IF_SCENE_NAME_IS_EMPTY

class TagHandlerCollectorDataBlock(TagHandler):
    def __init__(self,collector):
        self.collector = collector
        pass

    def _onExecute(self):
        name = self.node.getAttribute("Name")
        if name == "":
            name = ATLAS_NAME_IF_SCENE_NAME_IS_EMPTY
            pass

        self.collector.openSection(name)

        return True
        pass

    def _onFinalise(self):
        self.collector.closeSection()
        pass
    pass
