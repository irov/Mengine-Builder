__author__ = 'human88998999877'

def maxSort(val1, val2, first, second):
    if val1 > val2:
        return first,second
        pass

    return second, first
    pass

def minSort(val1, val2, first, second):
    if val1 < val2:
        return first,second
        pass

    return second, first
    pass

class PlaceHeuristicException(BaseException):
    pass

class PlaceHeuristic(object):
    def choose(self, rect, first, second):
        if first is None and second is None:
            raise PlaceHeuristicException("PlaceHeuristic Incorrect arguments all is None")
            pass

        if first is None:
            return second,first
            pass

        if second is None:
            return first,second
            pass

        return self._choose(rect, first, second)
        pass

    def _choose(self, rect, first, second):
        raise NotImplementedError()
        pass
    pass

### SHELF
class PlaceHeuristicFirstFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        return first,second
        pass
    pass

class PlaceHeuristicBestWidthFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = first.width - rect.width
        leftOver2 = second.width - rect.width
        return minSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicWorstWidthFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = first.width - rect.width
        leftOver2 = second.width - rect.width
        return maxSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicBestHeightFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = first.height - rect.height
        leftOver2 = second.height - rect.height
        return minSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicWorstHeightFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = first.height - rect.height
        leftOver2 = second.height - rect.height
        return maxSort(leftOver1, leftOver2, first, second)
        pass
    pass

### GUILLOTINE

class PlaceHeuristicBestShortSideFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = min( first.width - rect.width, first.height - rect.height )
        leftOver2  = min( second.width - rect.width, second.height - rect.height )
        return minSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicWorstShortSideFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = min( first.width - rect.width, first.height - rect.height )
        leftOver2  = min( second.width - rect.width, second.height - rect.height )
        return maxSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicWorstLongSideFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = max( first.width - rect.width, first.height - rect.height )
        leftOver2 = max( second.width - rect.width, second.height - rect.height )
        return maxSort(leftOver1, leftOver2, first, second)
        pass
    pass


class PlaceHeuristicBestLongSideFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = max( first.width - rect.width, first.height - rect.height )
        leftOver2 = max( second.width - rect.width, second.height - rect.height )
        return minSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicBestAreaFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = first.area - rect.area
        leftOver2 = second.area - rect.area
        return minSort(leftOver1, leftOver2, first, second)
        pass
    pass

class PlaceHeuristicWorstAreaFit(PlaceHeuristic):
    def _choose(self, rect, first, second):
        leftOver1 = first.area - rect.area
        leftOver2 = second.area - rect.area
        return maxSort(leftOver1, leftOver2, first, second)
        pass
    pass

#MaxRects
class PlaceHeuristicBottomLeft(PlaceHeuristic):
    def _choose(self, rect, first, second):
        if first.top == second.top:
            if first.left <= second.left:
                return first,second
                pass
            return second,first
            pass

        return minSort(first.top, second.top, first, second)
        pass
    pass
