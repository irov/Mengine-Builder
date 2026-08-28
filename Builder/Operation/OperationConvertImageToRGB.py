from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem


class OperationConvertImageToRGB (Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.quality = params.pop("Quality")
        pass

    def _getInfo(self):
        return ("image %s  converting  to  RGB   %s" %  (self.sourcePath,self.destinationPath ) )
        pass

    def _onRun(self):
        #FIX ME
        dirName = FileSystem.getDirname(self.destinationPath)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        img = Image.open(self.sourcePath)
        imgMode = img.mode
        bands  = img.split()
        if imgMode in ["RGB" , "RGBA"]:
            red,green,blue = bands[0:3]
            imageRgb = Image.merge("RGB",(red,green,blue))
            imageRgb.save( self.destinationPath,"JPEG", quality = self.quality )
            return True
            pass

        else:
            ErrorHandler.error("Converting image  with mode  %s not supported by %s" % (imgMode,self))
            return False
            pass
        pass
