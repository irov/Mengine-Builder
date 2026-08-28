from Builder.Config.ConfigJson import ConfigJson

from Builder.Error.ErrorHandler import ErrorHandler

from Builder.Operation.Operation import Operation
from Builder.Operation.OperationManager import OperationManager

class OperationCopyFonts(Operation):
    def _onParams( self, params ):
        self.Path = params.pop("Path")
        self.fileSystemCursor = params.pop("fileSystemCursor")
        pass

    def copyFile(self, sourcePath, destinationPath):
        sourceFull = self.fileSystemCursor.getFileSourcePath(sourcePath)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destinationPath)

        if sourceFull != destinationFull:
            with OperationManager.runOperationChain() as oc:
                oc.addOperation('CopyFile', SourcePath=sourceFull, DestinationPath=destinationFull, Doc="OperationCopyFonts")
                pass
            pass

        return oc.isSuccess()
        pass

    def _getInfo(self):
        return "source %s" % (self.Path)
        pass

    def _onRun(self):
        self.copyFile(self.Path, self.Path)

        FontJson = ConfigJson()

        FontPath = self.fileSystemCursor.getFileSourcePath(self.Path)
        FontJson.read(FontPath)

        if "GAME_FONTS" not in FontJson:
            ErrorHandler.error("You must determine GAME_FONTS in %s" % (FontPath, ))
            return False
            pass

        GAME_FONTS = FontJson["GAME_FONTS"]

        Fonts = []
        if "Font" in GAME_FONTS:
            FontName = GAME_FONTS["Font"]
            if isinstance(FontName, str) is True:
                Fonts.append(FontName)
                pass
            else:
                Fonts += FontName
                pass
            pass

        for FontName in Fonts:
            if FontName not in FontJson:
                ErrorHandler.error("You must determine Font %s in %s" % (FontName, FontPath))
                return False
                pass

            Font = FontJson[FontName]

            Type = Font["Type"]

            if Type == "Bitmap":
                #Empty
                pass
            elif Type == "TTF":
                if "FEPath" in Font:
                    FEPath = Font["FEPath"]
                    self.copyFile(FEPath, FEPath)
                    pass
                pass
            pass

        return True
        pass
