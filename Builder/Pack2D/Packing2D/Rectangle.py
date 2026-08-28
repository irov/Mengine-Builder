class Rectangle:
    @classmethod
    def fromBB(cls, left, top, right, bottom):
        rect = cls(0, 0, 0, 0)
        rect.setBB(left, top , right, bottom)
        return rect
        pass

    @classmethod
    def new(cls):
        rect = cls(0, 0, 0, 0)
        return rect
        pass

    @classmethod
    def fromRectangle(cls, rect):
        rect = cls(rect.left, rect.top, rect.width, rect.height)
        return rect
        pass

    @classmethod
    def fromWH(cls, width, height):
        rect = cls(0, 0, width, height)
        return rect
        pass

    def __init__(self, x, y, width, height):
        self.set(x, y, width, height)
        self._onInit()
        pass

    def _onInit(self):
        pass

    def set(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        pass

    def setBB(self, left, top, right, bottom):
        self.set(left, top, (right - left), (bottom - top))
        pass

    def setCoord(self, x, y):
        self._x = x
        self._y = y
        pass

    def isZeroSize(self):
        if self.left == 0 and self.width == 0 and self.top == 0 and self.height == 0:
            return True
            pass

        return False
        pass

    def getArea(self):
        return self.width * self.height
        pass

    area = property(fget=getArea)

    def getBBox(self):
        return ( self.left, self.top, self.right , self.bottom )
        pass

    def getWidth(self):
        return self._getWidth()
        pass

    def _getWidth(self):
        return  self._width
        pass

#    def setWidth(self, width):
#        raise NotImplemented()
#        self._width = width
#        pass
#
    width = property(fget = getWidth)

    def getHeight(self):
        return self._getHeight()
        pass

    def _getHeight(self):
        return self._height
        pass

#    def setHeight(self, height):
#        raise NotImplemented()
#        self._height = height
#        pass

    height = property(fget = getHeight)

    def getLeft(self):
        return self._x
        pass

    left = property(fget=getLeft)

    def getRight(self):
        if self.width is None:
            return
        return self.left + self.width
        pass

    right = property(fget=getRight)

    def getTop(self):
        return self._y
        pass

    top = property(fget=getTop)

    def getBottom(self):
        return self.top + self.height
        pass

    bottom = property(fget=getBottom)

    def getLongerSide(self):
        if self.width > self.height:
            return self.width
            pass

        return self.height
        pass

    def getShorterSide(self):
        if self.width < self.height:
            return self.width
            pass

        return self.height
        pass

    def isContain(self, rect):
        if self.right < rect.right \
            or self.bottom < rect.bottom \
            or self.left > rect.left \
            or self.top >  rect.top:
            return False
            pass

        return True
        pass

    def isPossibleToFit(self, rect):
        if self.height < rect.height or self.width < rect.width:
            return False
            pass

        return True
        pass

    def isIntersect(self, rect):
        if self.left >= rect.right or self.top >= rect.bottom or self.right <= rect.left or self.bottom <= rect.top:
            return False
            pass

        return True
        pass

    def getIntersection(self, rect):
        if self.isIntersect(rect) is False:
            return None
            pass

        left = max(self.left, rect.left)
        top = max(self.top,rect.top)
        width = min(self.width, rect.width)
        height = min(self.height, rect.height)
        return Rectangle(left, top, width, height)
        pass

    def __repr__(self):
        return "Rectangle %s : %s <left %d top : %d right : %d bottom: %d>" % (str(self.__class__.__name__), hex(id(self)), self.left, self.top, self.right, self.bottom)
        pass
    pass
