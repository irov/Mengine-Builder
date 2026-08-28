class Field2D(object):
    def __init__(self, data, width, height):
        super(Field2D, self).__init__()
        self.data = data
        self.width = width
        self.height = height
        pass

    def copyLine(self, field2d, y1, y2):
        for x1 in range(0, self.width):
            index1 = self.width * y1 + x1
            index2 = self.width * y2 + x1
            field2d.data[index2] = self.data[index1]
            pass
        pass

    def copyColumn(self, field2d, x1, x2):
        for y1 in range(0, self.height):
            index1 = self.width * y1 + x1
            index2 = field2d.width * y1 + x2
            field2d.data[index2] = self.data[index1]
            pass
        pass
