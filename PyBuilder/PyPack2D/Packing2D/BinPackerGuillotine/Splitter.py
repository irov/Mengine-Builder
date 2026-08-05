__author__ = 'human88998999877'

from PyBuilder.PyPack2D.Packing2D.Rectangle import Rectangle

class Splitter(object):
    def split(self, hostRect, rect):
        return self._onSplit(hostRect, rect)
        pass

    def _onSplit(self, hostRect, rect):
        raise NotImplementedError()
        pass
    pass

class SplitterHorizontal(Splitter):
    def _onSplit(self, hostRect, rect):
        first = Rectangle(hostRect.left+rect.width, hostRect.top, hostRect.width - rect.width, rect.height)
        second = Rectangle(hostRect.left, hostRect.top+rect.height, hostRect.width, hostRect.height - rect.height)
        return first,second
        pass
    pass

class SplitterVertical(Splitter):
    def _onSplit(self, hostRect, rect):
        first = Rectangle(hostRect.left+rect.width, hostRect.top, hostRect.width - rect.width, hostRect.height)
        second = Rectangle(hostRect.left, hostRect.top+rect.height, rect.width, hostRect.height - rect.height)
        return first,second
        pass
    pass

class SplitterShorterAxis(Splitter):
    def _onSplit(self, hostRect, rect):
        splitter = None
        if hostRect.width < hostRect.height:
            splitter = SplitterHorizontal()
            pass
        else:
            splitter = SplitterVertical()
            pass

        return splitter.split(hostRect, rect)
        pass
    pass


class SplitterShorterLeftOverAxis(Splitter):
    def _onSplit(self, hostRect, rect):
        splitter = None
        if (hostRect.width - rect.width) < (hostRect.height - rect.height):
            splitter = SplitterHorizontal()
            pass
        else:
            splitter = SplitterVertical()
            pass

        return splitter.split(hostRect, rect)
        pass
    pass

class SplitterLongerAxis(Splitter):
    def _onSplit(self, hostRect, rect):
        splitter = None
        if hostRect.width >= hostRect.height:
            splitter = SplitterHorizontal()
            pass
        else:
            splitter = SplitterVertical()
            pass

        return splitter.split(hostRect, rect)
        pass
    pass

class SplitterLongerLeftOverAxis(Splitter):
    def _onSplit(self, hostRect, rect):
        splitter = None
        if (hostRect.width - rect.width) >= (hostRect.height - rect.height):
            splitter = SplitterHorizontal()
            pass
        else:
            splitter = SplitterVertical()
            pass

        return splitter.split(hostRect, rect)
        pass
    pass

class SplitterMaxArea(Splitter):
    def _onSplit(self, hostRect, rect):
        splitterVertical = SplitterVertical()
        ver1,ver2 = splitterVertical.split(hostRect, rect)
        minVer = min(ver1.area, ver2.area)
        splitterHorizontal = SplitterHorizontal()
        hor1,hor2 = splitterHorizontal.split(hostRect, rect)
        minHor = min(hor1.area, hor2.area)
        if minHor < minVer:
            return hor1,hor2
            pass

        return ver1,ver2
        pass
    pass

class SplitterMinArea(Splitter):
    def _onSplit(self, hostRect, rect):
        splitterVertical = SplitterVertical()
        ver1,ver2 = splitterVertical.split(hostRect, rect)
        minVer = max(ver1.area, ver2.area)
        splitterHorizontal = SplitterHorizontal()
        hor1,hor2 = splitterHorizontal.split(hostRect, rect)
        minHor = max(hor1.area, hor2.area)
        if minHor > minVer:
            return hor1,hor2
            pass

        return ver1,ver2
        pass
    pass
