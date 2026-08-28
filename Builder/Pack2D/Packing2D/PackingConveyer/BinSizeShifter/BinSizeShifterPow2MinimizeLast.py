__author__ = 'human88998999877'
from Builder.Pack2D.Packing2D.PackingConveyer.BinSizeShifter.BinSizeShifterPow2 import BinSizeShifterPow2,getLowPow2

def findLowPow2(x):
    if x <= 8:
        return None
        pass

    y = 1
    z = y
    while True:
        if y > x:
            return z
            pass

        z = y
        y *= 2
        pass
    pass

class BinSizeShifterPow2MinimizeLast(BinSizeShifterPow2):
    def _onEndToPack(self, result):
        #TODO FIXME
        if len(result) == 0:
            return True
            pass

        #get last binSet and try to pack all it bins to smaller
        index = len(result) - 1
        minimized = self.findMinimalSize(result[index])
        #minimize all binSets
        super(BinSizeShifterPow2, self)._onEndToPack(result)

        #compare last minimized binSet with old last binSet
        self.normaliseSize(minimized)
        old = result[index]
        if old.getEfficiency() < minimized.getEfficiency():
            result[index] = minimized
            pass

        return True
        pass

    def findMinimalSize(self, binSet):
        binWidth = binSet.getWidth()
        binHeight = binSet.getHeight()

        binWidth2 = findLowPow2(binWidth)
        binHeight2 = findLowPow2(binHeight)

        if binWidth2 is None or binHeight2 is None:
            return binSet
            pass

        width = getLowPow2(binWidth2)
        height = getLowPow2(binHeight2)

        if width is None or height is None:
            return binSet
            pass

        self.packer.setSize(int(width), int(height))
        bins = binSet.getBins()
        for bin in bins:
            clone = bin.clone()
            if self.packer.packBin(clone) is False:
                return binSet
                pass
            pass

        result = self.packer.flush()
        return self.findMinimalSize(result)
        pass
    pass
