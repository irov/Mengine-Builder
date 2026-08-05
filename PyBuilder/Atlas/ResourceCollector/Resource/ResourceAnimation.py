__author__ = 'human88998999877'
from PyBuilder.Atlas.ResourceCollector.Resource.Resource import Resource

class ResourceAnimation(Resource):
    def getImageResources(self):
        images = []
        resourceNames = []

        children = self.node.getChildren()
        for child in children:
            tagName = child.getTagName()
            if tagName !="Sequence":
                continue
                pass

            resourceName = child.getAttribute("ResourceImageName")
            if resourceName in resourceNames:
                continue
                pass

            resourceNames.append(resourceName)

            resource = self.collector.getResource(resourceName, "ResourceAnimation")

            if resource is None:
                continue
                pass

            resType = resource.getType()
            if resType == "ResourceImageDefault":
                images.append(resource)
                pass
            pass

        return images
        pass
    pass
