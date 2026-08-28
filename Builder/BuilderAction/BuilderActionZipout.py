from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Operation.OperationManager import OperationManager
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
from Builder import Constants

import os
import shutil
import datetime

class BuilderActionZipout(BuilderAction):
    def _onRun(self):
        ErrorHandler.importantMessage("BuilderActionZipout '%s' to '%s'" % (self.project.destinationDir, self.project.Zipout))

        now = datetime.datetime.now()
        ErrorHandler.importantMessage("type %s"%(type(self.project.Zipout)))
        ErrorHandler.importantMessage("now year %s month %s day %s"%(now.year, now.month, now.day))

        Zipout = (self.project.Zipout).format(now.year, now.month, now.day)

        shutil.make_archive(Zipout, 'zip', self.project.destinationDir)
        pass
    pass
