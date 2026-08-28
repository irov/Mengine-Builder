from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
import os

from Builder.OSSystem import OSSystem

class OperationChangeIcons(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.iconsPath = params.pop("IconsPath")
        self.iconsName = params.pop("IconsName")
        pass

    def _getInfo(self):
        return  "source  %s \n\r destiny %s " %  (self.sourcePath, self.iconsPath)
        pass

    def _onRun(self):
        if FileSystem.isFile(self.iconsPath) is False:
            ErrorHandler.error("Icon file '%s' doesn't exist" % self.iconsPath)
            return False
            pass

        #* for resHacker v 3.6.0
        # toolFile = FileSystem.joinAndNormalisePath("tools\\resHacker","ResHacker.exe")

#            commandLine = "%s -delete %s, %s, ICONGROUP,,"  % (toolFile, self.sourcePath, self.sourcePath )
#            os.system(commandLine)
#            commandLine = "%s -addskip %s, %s, %s, ICONGROUP, %s, "  % (toolFile, self.sourcePath, self.sourcePath,  self.iconsPath, self.iconsName)
#            os.system(commandLine)
        # commandLine = "%s -modify %s, %s, %s, ICONGROUP, %s,"  % (toolFile, self.sourcePath, self.sourcePath,  self.iconsPath, "100")

        # * for resHacker v 5.1.8
        if OSSystem.tool(
            "ResourceHacker",
            "-open", self.sourcePath,
            "-save", self.sourcePath,
            "-action", "modify",
            "-res", self.iconsPath,
            "-mask", "ICONGROUP,100,MAINICON,100",
        ) is False:
            return False
            pass

        return True
        pass
    pass
