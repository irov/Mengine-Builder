from Builder.Pack2D.Packing2D.Rectangle import Rectangle
from Builder.Pack2D.Packing2D.Border import Border

class BinBase(Rectangle):
    def _onInit(self):
        self.rotate = False
        self.border = Border(bbox = (0,0,0,0))
        pass

    def setBorder(self, border):
        self.border = border
        pass

    def getBorder(self):
        return self.border
        pass

    #overloaded
    def _getWidth(self):
        return self._width + self.border.width
        pass

    #overloaded
    def _getHeight(self):
        return self._height + self.border.height
        pass

    def getRectangleWithoutBorder(self):
        left = self.left + self.border.left
        top = self.top + self.border.top
        width = self.width - self.border.width
        height = self.height - self.border.height
        return Rectangle( left, top, width, height )
        pass

    def setRotate(self, rotate):
        if self.rotate == rotate:
            return
            pass

        self.rotate = rotate
        self.set(0, 0, self.height, self.width)
        pass

    def flip(self):
        if self.isRotate() is False:
            self.setRotate(True)
            pass
        else:
            self.setRotate(False)
            pass
        pass

    def rotateUpRight(self):
        if self.width <= self.height:
            return
            pass

        self.flip()
        pass

    def rotateSideWays(self):
        if self.width >= self.height:
            return
            pass

        self.flip()
        pass

    def isRotate(self):
        return self.rotate
        pass

    def getUV(self, width, height):
        left = (self.left + self.border.left) / width
        top = (self.top + self.border.top) / height
        right = (self.right - self.border.right) / width
        bottom = (self.bottom - self.border.bottom) / height

        uv = (left, top, right, bottom)
        return uv
        pass

#class BinShadow(BinBase):
#    def setBin(self, bin):
#        self.bin = bin
#        self.set(bin.x, bin.y, bin.width, bin.height)
#        self.setRotate(bin.getRotate())
#        pass
#
#    def apply(self):
#        self.bin.setCoord(self.x, self.y)
#        self.bin.setRotate(self.rotate)
#        pass

class Bin(BinBase):
#    id = 0
#
#    @staticmethod
#    def initInstance():
#        id = Bin.id
#        Bin.id += 1
#        return id
#        pass

    def clone(self):
        if self.rotate is True:
            bin = Bin(0, 0, self._height, self._width)
            pass
        else:
            bin = Bin(0, 0, self._width, self._height)
            pass

        bin.setBorder(self.border)
        bin.setRotate(self.rotate)
        bin.setId(self.id)
        return bin
        pass

    def _onInit(self):
        super(Bin, self)._onInit()
        self.id = None
        #self.id = Bin.initInstance()
        pass

    def setId(self, id):
        self.id = id
        pass

    def getId(self):
        return self.id
        pass
    pass
