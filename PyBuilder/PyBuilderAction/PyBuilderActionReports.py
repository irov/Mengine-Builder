__author__ = 'human88998999877'

from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Graph.GraphRootXmlDom import GraphRootXmlDom
from PyBuilder.Error.ErrorHandler import ErrorHandler

class PyBuilderActionReports(PyBuilderAction):
    def _onRun(self):
        unknownTags = GraphRootXmlDom.getUnknownTags()
        template = "unable to handle tag <%s> which parsed %i counts"
        for tagName in unknownTags:
            warning = template % (tagName,unknownTags[tagName])
            ErrorHandler.warning(warning)
            pass
        pass
    pass
