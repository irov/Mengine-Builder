__author__ = 'human88998999877'
from Builder.Pack2D.Packing2D.Rectangle import Rectangle

class Cell(Rectangle):
    def cut(self, width):
        self.setBB( self.left + width, self.top, self.right, self.bottom )
        pass

    def isOver(self):
        if self.width == 0 or self.height == 0:
            return True
            pass
        pass

    def canPlace(self, rect):
        if self.height < rect.height or  self.width < rect.width:
            return False
            pass

        return True
        pass

    def place(self, rect):
        left = self.left
        top = self.top
        destinationRect = Rectangle( left, top, rect.width, rect.height  )
        self.cut( rect.width )
        return destinationRect
        pass
    pass
