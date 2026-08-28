__author__ = 'human88998999877'

from Builder.Pack2D.Packing2D import BorderType
from Builder.Pack2D.Atlas.BorderDraw import BorderDrawEdge, BorderDrawRectangle

from Builder import Tools
class AtlasImage(object):
    def __init__(self, path = None, img = None):
        super(AtlasImage, self).__init__()
        if  path != None:
            self._initFromFilename(path)
            pass
        elif img is not None:
            self._initFromImage(img)
            pass

        self._initialise()
        self.uv = (0,0,0,0)
        self.bin = None
        pass

    def _initFromFilename(self, path):
        openImage = Tools.loadImage(path)

        if openImage is None:
            raise IOError()
            pass

        self.img = openImage
        self.path = path
        pass

    def _initFromImage(self, img):
        self.img = img
        self.path = None
        pass

    def __repr__(self):
        return "<%s %s (%i,%i)>" %( self.__class__.__name__, self.path, self.width, self.height)
        pass

    def getBin(self):
        return self.bin
        pass

    def _initialise(self):
        self.width = Tools.getImageWidth(self.img)
        self.height = Tools.getImageHeight(self.img)
        pass

    def getImagePIL(self):
        return self.img
        pass

    def getPath(self):
        return  self.path
        pass

    def getWidth(self):
        return self.width
        pass

    def getHeight(self):
        return self.height
        pass

    def setBin(self, bin):
        self.bin = bin

        if self.bin.isRotate():
            self.rotate()
            pass

        border = self.bin.getBorder()

        if border.isEmpty() is True:
            return
            pass

        self.drawBorder(border)
        pass

    def rotate(self):
        self.img = Tools.rotateImage(self.img, -90)

        self._initialise()
        pass

    def drawBorder(self, border):
        draw = None
        if border.type == BorderType.PIXELS_FROM_EDGE:
            draw = BorderDrawEdge()
            pass
        elif border.type == BorderType.SOLID:
            draw = BorderDrawRectangle()
            pass

        self.img = draw.draw(self, border)

        self._initialise()
        pass

    def getUV(self):
        return self.uv
        pass

    def isRotate(self):
        return self.bin.isRotate()
        pass

    def pack(self, atlas):
        canvas = atlas.getCanvas()

        self.uv = self.bin.getUV(atlas.width, atlas.height)

        if self.bin is None:
            raise BaseException("Atlas Image pack error. Bin not determined")
            pass

        Tools.pasteImage(canvas, self.img, self.bin.left, self.bin.top)

        self._onPack(atlas)
        pass

    def pack2(self, atlas):
        self.uv = self.bin.getUV(atlas.width, atlas.height)

        if self.bin is None:
            raise BaseException("Atlas Image pack error. Bin not determined")
            pass

        self._onPack(atlas)
        pass

    def _onPack(self, atlas):
        pass

    def packEnd(self, atlas):
        self._onPackEnd(atlas)
        Tools.releaseImage(self.img)
        self.img = None
        pass

    def _onPackEnd(self, atlas):
        pass
    pass

class AtlasImageBuilder(AtlasImage):
    def __init__(self, path, onPackCallback = None):
        super(AtlasImageBuilder, self).__init__(path)
        self.onPackCallback = onPackCallback
        pass

    def _onPack(self, atlas):
        self.onPackCallback(self, atlas)
        pass
    pass
