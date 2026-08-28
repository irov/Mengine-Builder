__author__ = 'human88998999877'

from Builder.Pack2D.Packing2D.BinPacker.BinPacker import BinPacker
from Builder.Pack2D.Packing2D.BinPackerGuillotine.PackNode import PackNode

class BinPackerGuillotine(BinPacker):
    def _onInitialise(self, factory, settings):
        self.splitter = factory.getInstance(settings.splitRule)
        pass

    def _onSetSize(self):
        self.packNode =  PackNode(0, 0, self.maxWidth,  self.maxHeight)
        pass

    def _onPackBin(self, bin):
        leaf = self.packNode.insert( bin, self.splitter, self.heuristic )
        if leaf == None:
            return False
            pass

        bin.setCoord(leaf.left, leaf.top)
        return True
        pass

    def _onFlush(self):
        self.packNode =  PackNode(0, 0, self.maxWidth,  self.maxHeight)
        pass
    pass
