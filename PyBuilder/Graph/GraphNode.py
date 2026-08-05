class GraphNode(object):
    def getParent(self):
        pass

    def getChildren(self):
        pass

    def hasChildren(self):
        pass

    def createElement(self, resourceTag):
        pass

    def insertChildren(self, resource, nodeDom = None):
        pass

    def createChildren(self, resourceTag):
        pass

    def createChildrenFront(self, resourceTag):
        pass

    def getTagName(self):
        pass

    def getChildrenByTag(self, tagName):
        pass

    def getAttribute(self, attrName):
        pass

    def hasAttribute(self, attrName):
        pass

    def removeAttribute(self, attrName):
        pass

    def setAttribute(self, attrName, val):
        pass

    def removeFromParent(self):
        pass
    pass
