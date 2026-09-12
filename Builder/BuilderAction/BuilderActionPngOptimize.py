__author__ = 'human88998999877'
from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.TagHandler.TagHandlerPool import TagHandlerPool
from Builder.TagHandler.TagHandlerResource import TagHandlerResource
from Builder.TagHandler.TagHandlerResources import TagHandlerResources
from Builder.TagHandler.TagHandlerInclude import TagHandlerInclude
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageDefaultPngOptimize import ResourceHandlerImageDefaultPngOptimize

from Builder.PngOptimizer import PngOptimizer
from Builder.Watcher.Watcher import Watcher

class BuilderActionPngOptimize(BuilderAction):
    def _onInitialise(self):
        self.project.pngOptimizer = None
        return True

    def getPool(self):
        pool = TagHandlerPool(self.project)
        resourcePool = TagHandlerPool(self.project)

        resourcePool.setHandler("ResourceImageDefault", ResourceHandlerImageDefaultPngOptimize())
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

        if self.project.pngOptimizer.flush() is False:
            ErrorHandler.warning("invalid png optimizer flush [%s]", self.__repr__())

            return False
            pass

        return True
        pass

    def _onRun(self):
        Watcher.startInterval("PNGOPTIMIZE")
        self.project.pngOptimizer = PngOptimizer(self.project.logDir or self.project.destinationDir)
        try:
            return self.visitPacks()
        finally:
            Watcher.stopInterval("PNGOPTIMIZE")
        pass

    def _onFinalise(self):
        if self.project.pngOptimizer is not None:
            self.project.pngOptimizer.cleanup()
            self.project.pngOptimizer = None
        return True
        pass
    pass
