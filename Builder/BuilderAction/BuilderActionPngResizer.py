from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.TagHandler.TagHandlerPool import TagHandlerPool
from Builder.TagHandler.TagHandlerResource import TagHandlerResource
from Builder.TagHandler.TagHandlerResources import TagHandlerResources
from Builder.TagHandler.TagHandlerInclude import TagHandlerInclude
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageDefaultPngResizer import ResourceHandlerImageDefaultPngResizer

from Builder.Watcher.Watcher import Watcher

class BuilderActionPngResizer(BuilderAction):
    def getPool(self):
        pool = TagHandlerPool(self.project)
        resourcePool = TagHandlerPool(self.project)

        resourcePool.setHandler("ResourceImageDefault", ResourceHandlerImageDefaultPngResizer())

        pool.setHandler("Resource", TagHandlerResource(resourcePool))
        pool.setHandler("Include", TagHandlerInclude())
        pool.setHandler("Resources", TagHandlerResources())
        return pool
        pass

    def visitPacks(self):
        packs = self.project.getPacks()
        pool = self.getPool()

        for packName, pack in packs.items():
            if pack.visit(pool) is False:
                ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())
                return False
            pass

        return True
        pass

    def _onRun(self):
        Watcher.startInterval("PNGRESIZER")
        result = self.visitPacks()
        Watcher.stopInterval("PNGRESIZER")

        return True
        pass

    def _onFinalise(self):
        pass
    pass
