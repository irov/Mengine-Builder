from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.TagHandler.TagHandlerPool import TagHandlerPool
from PyBuilder.TagHandler.TagHandlerResource import TagHandlerResource
from PyBuilder.TagHandler.TagHandlerResources import TagHandlerResources
from PyBuilder.TagHandler.TagHandlerInclude import TagHandlerInclude
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageDefaultPngResizer import ResourceHandlerImageDefaultPngResizer

from PyBuilder.Watcher.Watcher import Watcher

class PyBuilderActionPngResizer(PyBuilderAction):
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
