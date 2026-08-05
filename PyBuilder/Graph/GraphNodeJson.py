from PyBuilder.Graph.GraphNode import GraphNode


class GraphNodeJson(GraphNode):
    def __init__(self, tagName, data, parent=None, parentContainer=None, parentKey=None):
        super(GraphNode, self).__init__()
        self.tagName = tagName
        self.data = data
        self.parent = parent
        self.parentContainer = parentContainer
        self.parentKey = parentKey
        pass

    @staticmethod
    def _isChildrenList(value):
        if isinstance(value, list) is False:
            return False

        return any(isinstance(item, (dict, list)) is True for item in value)

    @staticmethod
    def _attributeToString(value):
        if isinstance(value, list) is True:
            return " ".join(str(item) for item in value)

        if isinstance(value, bool) is True:
            return "1" if value is True else "0"

        return str(value)

    def getParent(self):
        return self.parent

    def createElement(self, resourceTag):
        return GraphNodeJson(resourceTag, {})

    def _insertChildData(self, resourceTag, data, node=None, front=False):
        if isinstance(self.data, dict) is False:
            raise TypeError("JSON graph node '%s' cannot contain children" % self.tagName)

        current = self.data.get(resourceTag)

        if current is None:
            self.data[resourceTag] = data
            return GraphNodeJson(resourceTag, data, self, self.data, resourceTag)

        if isinstance(current, dict) is True:
            children = [current]
            self.data[resourceTag] = children
        elif isinstance(current, list) is True:
            children = current
        else:
            raise TypeError("JSON field '%s' is an attribute, not a child collection" % resourceTag)

        if node is not None and isinstance(node, GraphNodeJson) and node.data in children:
            index = children.index(node.data)
        elif front is True:
            index = 0
        else:
            index = len(children)

        children.insert(index, data)
        return GraphNodeJson(resourceTag, data, self, children, None)

    def insertChildren(self, resource, node=None):
        if isinstance(resource, GraphNodeJson) is False:
            raise TypeError("resource must be a GraphNodeJson")

        return self._insertChildData(resource.tagName, resource.data, node=node)

    def createChildren(self, resourceTag, node=None):
        return self._insertChildData(resourceTag, {}, node=node)

    def createChildrenFront(self, resourceTag):
        return self._insertChildData(resourceTag, {}, front=True)

    def getChildren(self):
        if isinstance(self.data, dict) is False:
            return []

        children = []

        for key, value in self.data.items():
            if isinstance(value, dict) is True:
                child = GraphNodeJson(key, value, self, self.data, key)
                children.append(child)
                continue
                pass

            if self._isChildrenList(value) is True:
                for item in value:
                    child = GraphNodeJson(key, item, self, value, None)
                    children.append(child)
                    pass
                pass
            pass

        return children

    def hasChildren(self):
        return len(self.getChildren()) != 0

    def getTagName(self):
        return self.tagName

    def getChildrenByTag(self, tagName):
        children = []

        for child in self.getChildren():
            if child.getTagName() == tagName:
                children.append(child)
                pass

            children.extend(child.getChildrenByTag(tagName))
            pass

        return children

    def getChildByTag(self, tagName):
        return self.getChildrenByTag(tagName)[0]

    def getChildAttribute(self, tagName, attrName):
        return self.getChildByTag(tagName).getAttribute(attrName)

    def getAttribute(self, attrName):
        if self.hasAttribute(attrName) is False:
            return ""

        value = self.data[attrName]
        return self._attributeToString(value)

    def hasAttribute(self, attrName):
        if isinstance(self.data, dict) is False:
            return False

        if attrName not in self.data:
            return False

        value = self.data[attrName]

        if isinstance(value, dict) is True:
            return False

        if self._isChildrenList(value) is True:
            return False

        return True

    def removeAttribute(self, attrName):
        del self.data[attrName]
        pass

    def setAttribute(self, attrName, value):
        self.data[attrName] = value
        pass

    def removeFromParent(self):
        if self.parentContainer is None:
            return False

        if isinstance(self.parentContainer, dict) is True:
            del self.parentContainer[self.parentKey]
            return True

        self.parentContainer.remove(self.data)
        return True
    pass
