from Builder.Config.ConfigJson import ConfigJson

from Builder.Error.ErrorHandler import ErrorHandler

from Builder.Operation.Operation import Operation
from Builder.Operation.OperationManager import OperationManager

class OperationCopyGlyphs(Operation):
    def _onParams( self, params ):
        self.Path = params.pop("Path")
        self.fileSystemCursor = params.pop("fileSystemCursor")
        pass

    def copyFile(self, sourcePath, destinationPath):
        sourceFull = self.fileSystemCursor.getFileSourcePath(sourcePath)
        destinationFull = self.fileSystemCursor.getFileDestinationPath(destinationPath)

        if sourceFull != destinationFull:
            with OperationManager.runOperationChain() as oc:
                oc.addOperation('CopyFile', SourcePath=sourceFull, DestinationPath=destinationFull, Doc="OperationCopyGlyphs")
                pass
            pass

        return oc.isSuccess()
        pass

    def _getInfo(self):
        return "source %s" % (self.Path)
        pass

    def _onRun(self):
        self.copyFile(self.Path, self.Path)

        GlyphJson = ConfigJson()

        FontPath = self.fileSystemCursor.getFileSourcePath(self.Path)
        GlyphJson.read(FontPath)

        if "GAME_GLYPHS" not in GlyphJson:
            ErrorHandler.error("You must determine GAME_GLYPHS in %s" % (FontPath, ))
            return False
            pass

        GAME_GLYPHS = GlyphJson["GAME_GLYPHS"]

        Glyphs = []
        if "Glyph" in GAME_GLYPHS:
            GlyphName = GAME_GLYPHS["Glyph"]
            if isinstance(GlyphName, str) is True:
                Glyphs.append(GlyphName)
                pass
            else:
                Glyphs += GlyphName
                pass
            pass

        for GlyphName in Glyphs:
            if GlyphName not in GlyphJson:
                ErrorHandler.error("You must determine Glyph %s in %s" % (GlyphName, FontPath))
                return False
                pass

            Glyph = GlyphJson[GlyphName]

            Type = Glyph["Type"]

            if Type == "Bitmap":
                if "Description" in Glyph:
                    Description = Glyph["Description"]
                    self.copyFile(Description, Description)
                    pass

                if "Image" in Glyph:
                    Image = Glyph["Image"]
                    self.copyFile(Image, Image)
                    pass

                if "Outline" in Glyph:
                    Outline = Glyph["Outline"]
                    self.copyFile(Outline, Outline)
                    pass

                if "License" in Glyph:
                    License = Glyph["License"]
                    self.copyFile(License, License)
                    pass
                pass
            elif Type == "TTF":
                if "Path" in Glyph:
                    Path = Glyph["Path"]
                    self.copyFile(Path, Path)
                    pass

                if "License" in Glyph:
                    License = Glyph["License"]
                    self.copyFile(License, License)
                    pass
                pass
            pass

        return True
        pass
