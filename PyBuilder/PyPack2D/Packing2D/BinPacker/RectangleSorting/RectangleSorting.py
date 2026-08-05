from PyBuilder.PyPack2D.Packing2D import SortOrder
__author__ = 'human88998999877'

class RectangleSorting(object):
    def sort(self, input, order):
        isReverse = self.getReverseFromOrder(order)
        self._onSort(input, isReverse)
        pass

    def _onSort(self, input, isReverse):
        input.sort(key = lambda image: self.getSortingAttribute(image), reverse = isReverse)
        pass

    def getSortingAttribute(self, image):
        pass

    def getReverseFromOrder(self, order):
        if order == SortOrder.DESC:
            return True
            pass

        return False
        pass
    pass


class RectangleSortingArea(RectangleSorting):
    def getSortingAttribute(self, image):
        return image.getWidth() * image.getHeight()
        pass
    pass

class RectangleSortingWidth(RectangleSorting):
    def getSortingAttribute(self, image):
        return image.getWidth()
        pass
    pass

class RectangleSortingHeight(RectangleSorting):
    def getSortingAttribute(self, image):
        return image.getHeight()
        pass
    pass

class RectangleSortingShorterSide(RectangleSorting):
    def getSortingAttribute(self, image):
        width = image.getWidth()
        height = image.getHeight()
        if width < height:
            return width
            pass

        return height
        pass
    pass

class RectangleSortingLongerSide(RectangleSorting):
    def getSortingAttribute(self, image):
        width = image.getWidth()
        height = image.getHeight()
        if width > height:
            return width
            pass

        return height
        pass
    pass

class RectangleSortingPerimeter(RectangleSorting):
    def getSortingAttribute(self, image):
        width = image.getWidth()
        height = image.getHeight()
        return width + height
        pass
    pass

class RectangleSortingSideLengthDifference(RectangleSorting):
    def getSortingAttribute(self, image):
        width = image.getWidth()
        height = image.getHeight()
        return width - height
        pass
    pass

class RectangleSortingSideRatio(RectangleSorting):
    def getSortingAttribute(self, image):
        width = image.getWidth()
        height = image.getHeight()
        return width / height
        pass
    pass
