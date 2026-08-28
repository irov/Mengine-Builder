from Builder.Error.ErrorHandler import ErrorHandler

from Builder.TagHandler.TagHandlerPool import TagHandlerPool
from Builder.TagHandler.TagHandlerResource import TagHandlerResource
from Builder.TagHandler.TagHandlerResources import TagHandlerResources
from Builder.TagHandler.TagHandlerInclude import TagHandlerInclude

from Builder.Atlas.ResourceCollector.ResourceHandler.ResourceHandlerResourceCollector import ResourceHandlerResourceCollector
from Builder.Atlas.ResourceCollector.TagHandler.TagHandlerCollectorDataBlock import TagHandlerCollectorDataBlock

from Builder.Atlas.ResourceCollector.Resource.ResourceExternal import ResourceExternal
from Builder.Atlas.ResourceCollector.Resource.ResourceImageDefault import ResourceImageDefault
from Builder.Atlas.ResourceCollector.Resource.ResourceMovie import ResourceMovie
from Builder.Atlas.ResourceCollector.Resource.ResourceAnimation import ResourceAnimation

class ResourceCollectorSection(object):
    def __init__(self, name):
        super(ResourceCollectorSection, self).__init__()
        self.items = []
        self.name = name
        pass

    def getItems(self):
        return self.items
        pass

    def getName(self):
        return self.name
        pass

    def append(self, item):
        self.items.append(item)
        pass

    def empty(self):
        return len(self.items) == 0
        pass
    pass

class ResourceCollector(object):
    def __init__(self, project):
        super(ResourceCollector, self).__init__()
        self.project = project

        self.sections = []
        self.tags = {}
        self.sectionNames = {}
        self.currentSection = None
        self.isLockSection = False
        self.resources = {}

        #dict str=>boolean
        self.externalResources = {}
        pass

    def openSection(self, name):
        if self.isLockSection is True:
            return
            pass

        if self.currentSection is not None:
            ErrorHandler.error("ResourceCollector Resource Section doesn`t closed")
            pass

        if name not in self.sectionNames:
            section = ResourceCollectorSection(name)
            self.sectionNames[name] = section
            pass

        section = self.sectionNames[name]

        self.currentSection = section
        pass

    def closeSection(self):
        if self.isLockSection is True:
            return
            pass

        section = self.currentSection
        self.currentSection = None

        if section.empty() is True:
            return
            pass

        if section in self.sections:
            return
            pass

        self.sections.append(section)
        pass

    def lockSection(self):
        self.isLockSection = True
        pass

    def unlockSection(self):
        self.isLockSection = False
        pass

    def markExternal(self, resourceName):
        self.externalResources[resourceName] = True
        pass

    def isExternalResource(self, resourceName):
        if resourceName not in self.externalResources:
            return False
            pass

        return self.externalResources[resourceName]
        pass

    def addResource(self, name, resource):
        if resource.pool is not None:
            for tag in resource.pool.getTags():
                if tag not in self.tags:
                    self.tags[tag] = ResourceCollectorSection(tag)
                    pass

                self.tags[tag].append(resource)
                pass
            pass

        self.currentSection.append(resource)
        self.resources[name] = resource
        pass

    def getResource(self, name, doc):
        try:
            return self.resources[name]
            pass
        except (KeyError):
            ErrorHandler.warning("ResourceCollector Resource  doesn`t exist %s [%s]", name, doc)
            return None
            pass
        pass

    def getPool(self):
        pool = TagHandlerPool(self.project)
        resourcePool = TagHandlerPool(self.project)

        resourcePool.setHandler("ResourceImageDefault", ResourceHandlerResourceCollector(self, ResourceImageDefault))
        resourcePool.setHandler("ResourceExternal", ResourceHandlerResourceCollector(self, ResourceExternal))
        resourcePool.setHandler("ResourceMovie", ResourceHandlerResourceCollector(self, ResourceMovie))

        resourcePool.setHandler("ResourceAnimation", ResourceHandlerResourceCollector(self, ResourceAnimation))

        pool.setHandler("DataBlock", TagHandlerCollectorDataBlock(self))
        pool.setHandler("Resource", TagHandlerResource(resourcePool))

        pool.setHandler("Resources", TagHandlerResources())
        pool.setHandler("Include", TagHandlerInclude(self))
        return pool
        pass

    def collect(self, pack):
        pool = self.getPool()
        if pack.visit(pool) is False:
            ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())
            return False

        return True
        pass

    def getSections(self):
        return self.sections
        pass

    def getTags(self):
        return self.tags
        pass
    pass
