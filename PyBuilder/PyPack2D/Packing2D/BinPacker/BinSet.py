__author__ = 'human88998999877'

class BinSet(object):
    def __init__(self, width, height):
        super(BinSet, self).__init__()
        self.bins = []
        self.width = width
        self.height = height
        pass

    def getWidth(self):
        return self.width
        pass

    def getHeight(self):
        return self.height
        pass

    def setSize(self, width, height):
        self.width = width
        self.height = height
        pass

    def add(self, bin):
        self.bins.append(bin)
        pass

    def getBins(self):
        return self.bins
        pass

    def __iter__(self):
        return self.bins.__iter__()
        pass

    def empty(self):
        return len(self.bins) == 0
        pass

    def getEfficiency(self):
        area =  self.width * self.height
        binsArea = self.getBinsArea()
        efficiency = (binsArea * 100) / area
        return efficiency
        pass

    def getFreeSpace(self):
        area =  self.width * self.height
        binsArea = self.getBinsArea()
        return area - binsArea
        pass

    def getBinsArea(self):
        binsArea = 0
        for bin in self.bins:
            binsArea += bin.getArea()
            pass

        return binsArea
        pass
    pass
