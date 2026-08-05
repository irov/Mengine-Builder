__author__ = 'human88998999877'

from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler
import sys

class PyBuilderActionXlsxExport(PyBuilderAction):
    def _onInitialise(self):
        application_dir = FileSystem.getDirname(self.project.pathToApplicationJson)
        xlsxPath = FileSystem.joinAndNormalisePath(application_dir, "XlsxExport")

        if xlsxPath not in sys.path:
            sys.path.append(xlsxPath)

        return True
        pass

    def _onRun(self):
        CodeName = self.project.codeName
        ErrorHandler.importantMessage("Running XLSX Export %s" % CodeName)
        with OperationManager.runOperationChain(AutoRun=True) as oc:
            oc.addOperation("XlsxExport", CodeName=CodeName)
            pass
        return True
        pass
    pass
