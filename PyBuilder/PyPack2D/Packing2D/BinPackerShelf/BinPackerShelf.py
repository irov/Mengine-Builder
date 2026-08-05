__author__ = 'human88998999877'

from PyBuilder.PyPack2D.Packing2D.BinPacker.BinPacker import BinPacker
from PyBuilder.PyPack2D.Packing2D.BinPackerShelf.Shelf import Shelf

#TODO FLOOR CEILING

class BinPackerShelf(BinPacker):
    def _onInitialise(self, factory, settings):
        self.shelves = []
        pass

    def _onPackBin(self, bin):
        shelf = self.getShelf(bin, self.heuristic)

        #TODO ROTATE
        if shelf is None:
            return False
            pass

        destination = shelf.place(bin)

        bin.setCoord(destination.left, destination.top)
        return True
        pass

    def _onFlush(self):
        self.shelves = []
        pass

    def createNewShelf(self, bin):
        y = 0
        if len(self.shelves) != 0:
            topShelf = self.shelves[len(self.shelves) -1]
            y = topShelf.bottom
            pass

        if y + bin.height > self.maxHeight:
            return None
            pass

        shelf = Shelf(0, y, self.maxWidth, bin.height)
        self.shelves.append(shelf)
        return shelf
        pass

    def getShelf(self, bin, heuristic):
        bestShelf = None
        bestRect = None
        for shelf in self.shelves:
            if shelf.canPlace(  bin ) is False:
                continue
                pass

            rect = shelf.getFreeRect()
            best,worth = heuristic.choose(bin, bestRect, rect)

            if best is not bestRect:
                bestRect = best
                bestShelf = shelf
                pass
            pass

        if bestShelf is None:
            shelf = self.createNewShelf(bin)
            return shelf
            pass

        return bestShelf
        pass
    pass
