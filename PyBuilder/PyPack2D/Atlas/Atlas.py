from PyBuilder import Tools

from PyBuilder.Error.ErrorHandler import ErrorHandler

class Atlas(object):
    def __init__(self):
        super(Atlas,self).__init__()
        self.width = 0
        self.height = 0
        self.dirPath = None
        self.fileName = None
        self.textureMode = None
        self.atlasType = None
        self.fillColor = None

        self.canvas = None
        self.images = []
        self.images2 = []

        self.writenAtlases = []

        self.bound = [0,0]
        pass

    def initialise(self, width, height, dirPath, fileName, texMode, atlasType, fillColor):
        self.width = width
        self.height = height
        self.dirPath = dirPath
        self.fileName = fileName
        self.textureMode = texMode
        self.atlasType = atlasType
        self.fillColor = fillColor
        pass

    def finalize(self):
        self.canvas = None
        pass

    def addImage(self, image):
        self.images.append(image)
        pass

    def addImage2(self, image):
        self.images2.append(image)
        pass

    def updateBound(self, x, y):
        if (x >= self.bound[0]):
            self.bound[0] = x
            pass

        if (y >= self.bound[1]):
            self.bound[1] = y
            pass
        pass

    def getBound(self):
        return self.bound
        pass

    def addWritenAtlas(self, atlasPath):
        self.writenAtlases.append(atlasPath)
        pass

    def getWritenAtlases(self):
        return self.writenAtlases
        pass

    def getCanvas(self):
        return self.canvas
        pass

    def crop(self):
        self.canvas = self.canvas.crop((0, 0, int(self.bound[0] * self.width) , int(self.bound[1] * self.height)))
        pass

    def save(self):
        path = self.dirPath + "/" + self.fileName
        if Tools.saveImage(self.canvas, path) is False:
            ErrorHandler.warning("invalid save image [%s] path [%s]", self.__repr__(), path)

            return False
            pass

        return True
        pass

    def getFileName(self):
        path = self.dirPath + "/" + self.fileName
        return path
        pass

    def show(self):
        self.canvas.show()
        pass

    def pack(self):
        channels = 3 if self.textureMode == "RGB" else 4

        self.canvas = Tools.createImage(self.width, self.height, channels, self.fillColor)

        for img in self.images:
            img.pack(self)
            pass

        for img in self.images2:
            img.pack2(self)
            pass

        for img in self.images:
            imUV = img.getUV()
            self.updateBound(imUV[2], imUV[3])
            pass

        for img in self.images:
            img.packEnd(self)
            pass

        self.images = []
        pass
    pass
