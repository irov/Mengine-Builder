__author__ = 'human88998999877'
from PyBuilder.Atlas.ResourceCollector.Resource.Resource import Resource

class ResourceExternal(Resource):
    def _onInitialise(self):
        self.collector.markExternal(self.getName())

        return True
        pass

    def getImageResources(self):
        externals = self.node.getChildren()
        images = []

        for external in externals:
            name = external.getAttribute("Name")

            resource = self.collector.getResource(name, "ResourceExternal")
            if resource is None:
                continue
                pass

            resources = resource.getImageResources()
            images.extend(resources)
            pass

        return images
        pass
    pass
