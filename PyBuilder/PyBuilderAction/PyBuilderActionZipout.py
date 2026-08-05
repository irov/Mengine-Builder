from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder import Constants

import os
import shutil
import datetime

class PyBuilderActionZipout(PyBuilderAction):
    def _onRun(self):
        ErrorHandler.importantMessage("PyBuilderActionZipout '%s' to '%s'" % (self.project.destinationDir, self.project.Zipout))

        now = datetime.datetime.now()
        ErrorHandler.importantMessage("type %s"%(type(self.project.Zipout)))
        ErrorHandler.importantMessage("now year %s month %s day %s"%(now.year, now.month, now.day))

        Zipout = (self.project.Zipout).format(now.year, now.month, now.day)

        shutil.make_archive(Zipout, 'zip', self.project.destinationDir)
        pass
    pass
