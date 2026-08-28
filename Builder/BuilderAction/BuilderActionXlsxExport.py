__author__ = 'human88998999877'

from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Operation.OperationManager import OperationManager
from Builder.FileSystem import FileSystem
from Builder.Error.ErrorHandler import ErrorHandler
import sys

class BuilderActionXlsxExport(BuilderAction):
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
