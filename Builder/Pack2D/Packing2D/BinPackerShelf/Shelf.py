__author__ = 'human88998999877'
from Builder.Pack2D.Packing2D.Rectangle import Rectangle

class Shelf(Rectangle):
    def _onInit(self):
        self.bins = []
        self.freeRect = Rectangle(self.left, self.top, self.width, self.height)
        pass

    def getFreeRect(self):
        return self.freeRect
        pass

    def canPlace(self, rect):
        if self.freeRect.height < rect.height or  self.freeRect.width < rect.width:
            return False
            pass

        return True
        pass

    def isEmpty(self):
        return len(self.bins) == 0
        pass

    def place(self, bin):
        destinationRect = Rectangle( self.freeRect.left, self.freeRect.top, bin.width, bin.height  )

        self.freeRect = Rectangle.fromBB( destinationRect.right, self.freeRect.top, self.right, self.bottom )
        self.bins.append(bin)
        return destinationRect
        pass
    pass
