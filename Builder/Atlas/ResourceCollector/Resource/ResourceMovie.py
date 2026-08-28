__author__ = 'human88998999877'
from Builder.Atlas.ResourceCollector.Resource.Resource import Resource

class ResourceMovie(Resource):
    def getImageResources(self):
        imageResources = []
        images = []

        children = self.node.getChildren()
        for child in children:
            tagName = child.getTagName()
            if tagName !="MovieLayer2D":
                continue
                pass

            resourceName = child.getAttribute("Source")
            if resourceName in imageResources:
                continue
                pass

            imageResources.append(resourceName)
            resource = self.collector.getResource(resourceName, "ResourceMovie")

            if resource is None:
                continue
                pass

            resType = resource.getType()
            if resType == "ResourceAnimation":
                resources = resource.getImageResources()
                images.extend(resources)
                pass
            if resType == "ResourceImageDefault":
                images.append(resource)
                pass
            pass

        return images
        pass
    pass
