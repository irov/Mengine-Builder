__author__ = 'human88998999877'

from PyBuilder.PyPack2D.Packing2D.BinPacker.BinPacker import BinPacker

#TODO DEBUG AND AREA TO BASIC

from PyBuilder.PyPack2D.Packing2D.BinPackerMaxRectangles.Area import Area

class BinPackerMaxRectangles(BinPacker):
    def _onInitialise(self, factory, settings):
        self.waste = []
        pass

    def _onSetSize(self):
        self.areas = [Area.fromWH(self.maxWidth,self.maxHeight)]
        pass

    def _onPackBin(self, bin):
        bestRect = self.getBestRectangle(bin, self.heuristic)

        if bestRect is None:
            return False
            pass

        destination = self.placeBinToRect(bestRect, bin)
        bin.setCoord(destination.left, destination.top)
        return True
        pass

    def placeBinToRect(self, rect, bin):
        destination = Area(rect.left, rect.top, bin.width, bin.height)
        self.splitOnMaxRectangles(rect, destination, self.areas)
        self.areas.remove(rect)
        self.checkBinIntersections(destination)
        self.normaliseRectangles()
        return destination
        pass

    def checkBinIntersections(self, bin):
        newRects = []

        for rect in self.areas:
            intersection = rect.getIntersection(bin)
            if intersection is None:
                continue
                pass

            self.splitOnMaxRectangles(rect, intersection, newRects)
            self.waste.append(rect)
            pass

        if len(newRects) == 0:
            return
            pass

        self.removeBad()
        self.areas.extend(newRects)
        pass

    def normaliseRectangles(self):
        sortedAreas = sorted(self.areas, key = lambda rect: rect.getArea(), reverse = False)

        for i in range(len(sortedAreas)):
            checked = sortedAreas[i]
            for rect in sortedAreas[i + 1 : len(self.areas)]:
                if rect.isContain(checked):
                    self.waste.append(checked)
                    break
                    pass
                pass
            pass

        self.removeBad()
        pass

    def removeBad(self):
        for area in self.waste:
            self.areas.remove(area)
            pass

        self.waste = []
        pass

    def splitOnMaxRectangles(self, bigRect, splitRect, destination):
        if splitRect.left != bigRect.left:
            rect = Area(bigRect.left, bigRect.top, splitRect.left - bigRect.left, bigRect.height)
            destination.append(rect)
            pass

        if splitRect.top != bigRect.top:
            rect = Area(bigRect.left, bigRect.top, bigRect.width, splitRect.top - bigRect.top)
            destination.append(rect)
            pass

        if splitRect.right != bigRect.right:
            rect = Area(splitRect.right, bigRect.top, bigRect.right - splitRect.right,  bigRect.height)
            destination.append(rect)
            pass

        if splitRect.bottom != bigRect.bottom:
            rect = Area(bigRect.left, splitRect.bottom, bigRect.width, bigRect.bottom - splitRect.bottom)
            destination.append(rect)
            pass
        pass

    def getBestRectangle(self, bin, heuristic):
        bestRect = None
        for rect in self.areas:
            if rect.isPossibleToFit(bin) is False:
                continue
                pass

            best,worth = heuristic.choose(bin, bestRect, rect)

            if best is not bestRect:
                bestRect = best
                pass
            pass

        return bestRect
        pass

    def _onDebug(self):
        return
        pass
    pass
