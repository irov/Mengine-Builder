__author__ = 'human88998999877'

from Builder.Pack2D.Packing2D.PackingConveyer.BinSizeShifter.BinSizeShifter import BinSizeShifter
from Builder.Pack2D.Packing2D.Rectangle import Rectangle

def getLowPow2( x ):
    y = 2
    if y > x:
        return None
    while True:
        if y >= x:
            return y / 2
            pass
        y *= 2
        pass
    pass

def getNearestPow2( x ):
    y = 1
    if y > x:
        return None
    while True:
        if y >= x:
            return y
            pass
        y *= 2
        pass
    pass

class BinSizeShifterPow2Square(BinSizeShifter):
    def _onShift(self, binSet):
        self.normaliseSize(binSet)
        pass

    def _normaliseSize(self, binSet, newWidth, newHeight):
        #print("normaliseSize")
        #print(newWidth,newHeight)

        newRect = Rectangle.fromWH(newWidth, newHeight)

        if self.canChangeRect(binSet, newRect) is False:
            #print("CANT CHANGE",newRect)
            return False
            pass

        binSet.setSize(int(newRect.width), int(newRect.height))
        return True
        pass
    pass

    def normaliseSize(self, binSet):
        newWidth = getLowPow2( binSet.getWidth() )
        newHeight = getLowPow2( binSet.getHeight() )

        if newWidth is None or newHeight is None:
            return False
            pass

        if self._normaliseSize(binSet, newWidth, newHeight) is False:
            return False
            pass

        self.normaliseSize(binSet)
        return True
        pass

    def canChangeRect(self, binSet, newRect):
        for bin in binSet:
            if newRect.isContain(bin) is False:
                return False
                pass
            pass

        return True
        pass
    pass
