__author__ = 'human88998999877'

from Builder.Pack2D.Packing2D.BinPacker.BinPacker import BinPacker
from Builder.Pack2D.Packing2D.BinPackerCell.Cell import Cell

class BinPackerCell(BinPacker):
    def _onSetSize(self):
        self.cells = [Cell( 0, 0, self.maxWidth, self.maxHeight )]
        pass

    def _onPackBin(self, bin):
        bestCell = self.getBestCell(bin)

        if bestCell is None:
            return False
            pass

        destinationRect = bestCell.place(bin)

        newLine = Cell( destinationRect.left, destinationRect.bottom, destinationRect.width, bestCell.height - bin.height )

        if bestCell.isOver() is True:
            self.cells.remove(bestCell)
            pass

        self.cells.append(newLine)

        self.normalise(destinationRect)

        bin.setCoord(destinationRect.left, destinationRect.top)
        return True
        pass

    def canPlace(self, cell, rect):
        if cell.height < rect.height:
            return False
            pass

        if cell.width >= rect.width:
            return True
            pass

        rightEdge = cell.left + rect.width

        if rightEdge > self.maxWidth:
            return False
            pass

        for bin in self.binSet:
            if bin.left < rightEdge and bin.bottom > cell.top:
                return False
                pass
            pass

        return True
        pass
    pass

    def getBestCell(self, bin):
        bestCell = None
        minTopLeft = self.maxHeight * 2
        for cell in self.cells:
            if self.canPlace( cell, bin ) is False:
                continue
                pass

            topLeft =  cell.top + bin.height

            if minTopLeft < topLeft:
                continue
                pass

            bestCell = cell
            minTopLeft = topLeft
            pass

        return bestCell
        pass

    def normalise(self, destinationRect):
        newCells = []
        for cell in self.cells:
            if cell.left < destinationRect.right \
               and cell.top < destinationRect.top :

                if cell.right < destinationRect.right:
                    cell.setBB( cell.left, cell.top, cell.right, destinationRect.top )
                    pass
                else:
                    newCell = Cell( cell.left, cell.top, destinationRect.right, destinationRect.top )
                    cell.cut( newCell.getWidth() )
                    newCells.append(newCell)
                    pass

                pass

        if len(newCells) != 0:
            self.cells.extend(newCells)
            pass
        pass
    pass
