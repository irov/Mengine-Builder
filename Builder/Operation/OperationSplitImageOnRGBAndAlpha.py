from Builder import Tools

from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem

class OperationSplitImageOnRGBAndAlpha(Operation):
    def _getInfo(self):
        return ("image %s  splitting by  RGB   %s \n\r alpha %s " %  (self.sourcePath,self.destinationPathRGB,self.destinationPathAlpha   ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPathRGB = params.pop("DestinationPathRGB")
        self.destinationPathAlpha = params.pop("DestinationPathAlpha")
        pass

    def _onRun(self):
        #FIX ME
        dirName = FileSystem.getDirname(self.destinationPathRGB)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)
        dirName = FileSystem.getDirname(self.destinationPathAlpha)
        FileSystem.makeDirsRecursiveIfNotExist(dirName)

        img = Tools.loadImage(self.sourcePath)

        imageRgb, imageAlpha = img.split()

        if Tools.saveImage(imageRgb, self.destinationPathRGB) is False:
            ErrorHandler.warning("invalid save image RGB [%s] source [%s] destination [%s]", self.__repr__(), self.sourcePath, self.destinationPathRGB)
            return False
            pass

        if Tools.saveImage(imageAlpha, self.destinationPathAlpha) is False:
            ErrorHandler.warning("invalid save image Alpha [%s] source [%s] destination [%s]", self.__repr__(),
                                 self.sourcePath, self.destinationPathAlpha)
            return False
            pass

        return True
        pass
    pass
