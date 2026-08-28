__author__ = 'human88998999877'

from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Graph.GraphRootXmlDom import GraphRootXmlDom
from Builder.Error.ErrorHandler import ErrorHandler

class BuilderActionReports(BuilderAction):
    def _onRun(self):
        unknownTags = GraphRootXmlDom.getUnknownTags()
        template = "unable to handle tag <%s> which parsed %i counts"
        for tagName in unknownTags:
            warning = template % (tagName,unknownTags[tagName])
            ErrorHandler.warning(warning)
            pass
        pass
    pass
