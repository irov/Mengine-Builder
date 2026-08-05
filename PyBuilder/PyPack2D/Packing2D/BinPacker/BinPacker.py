from PyBuilder.Error.ErrorHandler import ErrorHandler

from PyBuilder.PyPack2D.Packing2D.BinPacker.BinSet import BinSet
from PyBuilder.PyPack2D.Packing2D import BorderMode,RotateMode
from PyBuilder.PyPack2D.Packing2D.Border import Border

class BinPackerError(BaseException):
    pass

class ManualAbort(object):
    def __init__(self):
        super(ManualAbort,self ).__init__()
        self.debugCount = 0
        pass

    def abortOnCount(self, limit):
        if self.debugCount >= limit:
            raise BaseException()
            pass

        self.debugCount+=1
        pass
    pass

class BinPacker(object):
    def __init__(self):
        super(BinPacker,self ).__init__()
        pass

    def initialise(self, factory, settings):
        self.settings = settings
        self.heuristic = factory.getInstance(settings.placeHeuristic)

        self.settings = settings
        self._onInitialise( factory, settings )
        pass

    def setSize(self, width, height):
        self.maxWidth = width
        self.maxHeight = height

        if self.settings.borderMode == BorderMode.AUTO:
            self.maxHeight += self.settings.borderSize * 2
            self.maxWidth += self.settings.borderSize * 2
            pass

        self.binSet = BinSet(self.maxWidth, self.maxHeight)
        self._onSetSize()
        pass

    def _onSetSize(self):
        raise NotImplementedError()
        pass

    def _onInitialise(self, factory, settings):
        pass

    def packBin(self, bin):
        self.setBorder(bin)

        if self._onPackBin(bin) is False:
            return False
            pass

        if self.settings.isDebug is True:
            self.validate(bin)
            self.onDebug()
            pass

        self.binSet.add(bin)

        return True
        pass

    def validate(self, bin):
        for binCheck in self.binSet:
            if binCheck.isIntersect(bin) is True:
                raise BinPackerError( "Validate Error bins are intersected : %s with %s" % (binCheck,bin) )
                pass
            pass
        pass

    def onDebug(self):
        self._onDebug()
        pass

    def _onDebug(self):
        pass

    def _onPackBin(self, bin):
        raise NotImplementedError()
        pass

    def setBorder(self, bin):
        if self.settings.borderMode == BorderMode.NONE:
            return
            pass
        elif self.settings.borderMode == BorderMode.STRICT:
            border = Border(border=self.settings.border)
            bin.setBorder(border)
            pass
        elif self.settings.borderMode == BorderMode.AUTO:
            border = Border(borderSize=self.settings.borderSize, type=self.settings.border.type, color=self.settings.border.color)
            bin.setBorder(border)
            pass
        pass

    def normaliseBorder(self):

        realWidth = self.maxWidth - self.settings.borderSize * 2
        realHeight = self.maxHeight - self.settings.borderSize * 2
        for bin in self.binSet:
            border = bin.getBorder()
            if bin.top == 0:
                border.top = 0
                pass
            else:
                bin.setCoord(bin.left, bin.top - self.settings.borderSize)
                pass
            if bin.left == 0:
                border.left = 0
                pass
            else:
                bin.setCoord(bin.left - self.settings.borderSize, bin.top)
                pass
            if bin.right > realWidth:
                border.right = 0
                pass
            if bin.bottom > realHeight:
                border.bottom = 0
                pass
            pass


            self.binSet.setSize(realWidth, realHeight)
            pass
        pass

    def flush(self):
        if self.settings.borderMode == BorderMode.AUTO:
            self.normaliseBorder()
            pass

        result = self.binSet
        self.binSet = BinSet(self.maxWidth, self.maxHeight)
        self._onFlush()
        self._onSetSize()
        return result
        pass

    def _onFlush(self):
        pass
    pass
