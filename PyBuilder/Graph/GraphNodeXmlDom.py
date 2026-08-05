from PyBuilder.Graph.GraphNode import GraphNode
from xml.dom.minidom import Node
from xml.dom.minidom import Document

class GraphNodeXmlDom(GraphNode):
    def __init__(self, nodeXmlDom):
        super(GraphNode, self).__init__()
        self.nodeDom = nodeXmlDom
        pass

    def getXmlDomElement(self):
        return self.nodeDom
        pass

    def getParent(self):
        return GraphNodeXmlDom(self.nodeDom.parentNode)
        pass

    def getChildren(self):
        return [GraphNodeXmlDom(child) for child in self.nodeDom.childNodes if child.nodeType == Node.ELEMENT_NODE]
        pass

    def createElement(self, resourceTag):
        doc = Document()

        resource = doc.createElement(resourceTag)

        return GraphNodeXmlDom(resource)
        pass

    def insertChildren(self, resource, nodeDom = None):
        if nodeDom is None:
            self.nodeDom.appendChild(resource)
            pass
        else:
            self.nodeDom.insertBefore(resource, nodeDom.nodeDom)
            pass
        pass

    def createChildren(self, resourceTag, nodeDom = None):
        doc = Document()

        resource = doc.createElement(resourceTag)

        self.insertChildren(resource, nodeDom)

        return GraphNodeXmlDom(resource)
        pass

    def createChildrenFront(self, resourceTag):
        doc = Document()

        resource = doc.createElement(resourceTag)

        if self.nodeDom.firstChild is not None:
            self.nodeDom.insertBefore(resource, self.nodeDom.firstChild)
        else:
            self.nodeDom.appendChild(resource)
            pass

        return GraphNodeXmlDom(resource)
        pass

    def hasChildren(self):
        return self.nodeDom.hasChildNodes()
        pass

    def getTagName(self):
        if self.nodeDom.nodeType != Node.ELEMENT_NODE:
            return None
            pass

        return self.nodeDom.tagName
        pass

    def getChildrenByTag(self, tagName):
        return [GraphNodeXmlDom(child) for child in self.nodeDom.getElementsByTagName(tagName)]
        pass

    def getChildByTag(self, tagName):
        return [GraphNodeXmlDom(child) for child in self.nodeDom.getElementsByTagName(tagName)][0]
        pass

    def getChildAttribute(self, tagName, attrName):
        return [GraphNodeXmlDom(child) for child in self.nodeDom.getElementsByTagName(tagName)][0].getAttribute(attrName)
        pass

    def getAttribute(self, attrName):
        return self.nodeDom.getAttribute(attrName)
        pass

    def hasAttribute(self, attrName):
        return self.nodeDom.hasAttribute(attrName)
        pass

    def removeAttribute(self, attrName):
        self.nodeDom.removeAttribute(attrName)
        pass

    def setAttribute(self, attrName, val):
        self.nodeDom.setAttribute(attrName, val)
        pass

    def removeFromParent(self):
        if self.nodeDom.parentNode is None:
            return False
            pass

        self.nodeDom.parentNode.removeChild(self.nodeDom)
        pass

    def toprettyxml(self, encoding, indent, newl):
        return self.nodeDom.toprettyxml(indent, newl, encoding)
        pass
