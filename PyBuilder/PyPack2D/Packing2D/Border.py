class Border(object):
    def __init__(self, bbox=None, border=None, borderSize=None, type=None, color=None):
        if bbox is not None:
            self.init(bbox[0], bbox[1], bbox[2], bbox[3], type, color)
            pass
        elif border is not None:
            self.init(border.left, border.top, border.right, border.bottom, border.type, border.color)
            return
            pass
        elif borderSize is not None:
            self.init(borderSize, borderSize, borderSize, borderSize, type, color)
            pass
        pass

    def init(self, left, top, right, bottom, type=None, color=None):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.type = type
        self.color = color
        pass

    def isEmpty(self):
        if self.left == 0 and self.right == 0 and self.top == 0 and self.bottom == 0:
            return True
            pass

        return False
        pass

    def getWidth(self):
        return self.left + self.right
        pass

    width = property(fget=getWidth)

    def getHeight(self):
        return self.top + self.bottom
        pass

    height = property(fget=getHeight)
    pass
