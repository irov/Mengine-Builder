__author__ = 'human88998999877'
from PyBuilder.Atlas.ResourceCollector.Resource.Resource import Resource

from PyBuilder.PyPack2D.Atlas.AtlasImage import AtlasImage

from PyBuilder.FileSystem import FileSystem
from PyBuilder.Environment import Environment
import PyBuilder.Constants as Constants

import ToolsBuilderPlugin

class AtlasImagePyBuilder(AtlasImage):
    def __init__(self, path=None, img=None, onPackCallback=None, onPackCallbackEnd=None):
        super(AtlasImagePyBuilder, self).__init__(path, img)
        self.onPackCallback = onPackCallback
        self.onPackCallbackEnd = onPackCallbackEnd
        self.path = path
        pass

    def _onPack(self,atlas):
        self.onPackCallback(self, atlas)
        pass

    def _onPackEnd(self,atlas):
        self.onPackCallbackEnd(self, atlas)
        pass

    def getImagePath(self):
        return self.path
        pass
    pass


class ResourceImageDefault(Resource):
    def _onSkip(self):
        self.fileNode = self.getFileNode()

        if self.fileNode.hasAttribute("NoAtlas"):
            if self.fileNode.getAttribute("NoAtlas") == "1":
                return True
                pass
            pass

        if self.fileNode.hasAttribute("NoConvert"):
            if self.fileNode.getAttribute("NoConvert") == "1":
                return True
                pass
            pass

        if self.fileNode.hasAttribute("NoExist"):
            if self.fileNode.getAttribute("NoExist") == "1":
                return True
                pass
            pass

        return False
        pass

    def _onInitialise(self):
        return True
        pass

    def getFileNode(self):
        children = self.node.getChildren()
        for child in children:
            tagName = child.getTagName()
            if tagName == "File":
                return child
                pass
            pass
        pass

    def __makeUV(self, uv, isRotate):
        uv4 = [0.0]*8

        if isRotate is False:
            uv4[0] = uv[0]
            uv4[1] = uv[1]
            uv4[2] = uv[2]
            uv4[3] = uv[1]
            uv4[4] = uv[2]
            uv4[5] = uv[3]
            uv4[6] = uv[0]
            uv4[7] = uv[3]
        else:
            uv4[0] = uv[2]
            uv4[1] = uv[1]
            uv4[2] = uv[2]
            uv4[3] = uv[3]
            uv4[4] = uv[0]
            uv4[5] = uv[3]
            uv4[6] = uv[0]
            uv4[7] = uv[1]
            pass

        uvStr = "%.16f;%.16f;%.16f;%.16f;%.16f;%.16f;%.16f;%.16f" % tuple(uv4)

        return uvStr
        pass

    def __replaceFileNodeNoConvert(self, filename, __Dir, uvStr, uvRotate, MaxSize, Size, Offset, alpha):
        self.node.setAttribute("Type", "ResourceImageSubstract")

        if self.fileNode is not None:
            self.fileNode.removeFromParent()
            pass

        resourceImageNode = self.node.createChildren("Image")

        resourceImageNode.setAttribute("Name", filename)
        resourceImageNode.setAttribute("UV", uvStr)
        resourceImageNode.setAttribute("UVRotate", uvRotate)
        resourceImageNode.setAttribute("Alpha", alpha)
        resourceImageNode.setAttribute("MaxSize", MaxSize)

        if __Dir is not None:
            resourceImageNode.setAttribute("__Dir", __Dir)
            pass

        if Size is not None:
            resourceImageNode.setAttribute("Size", Size)
            pass

        if Offset is not None:
            resourceImageNode.setAttribute("Offset", Offset)
            pass

        self.setAlreadyInAtlas()
        pass

    def __replaceFileNodeWebp(self, filename, __Dir, uvStr, uvRotate, MaxSize, Size, Offset, alpha):
        self.node.setAttribute("Type", "ResourceImageSubstract")

        if self.fileNode is not None:
            self.fileNode.removeFromParent()
            pass

        resourceImageNode = self.node.createChildren("Image")

        PathWebp = FileSystem.setFileExtension(filename, "webp")

        resourceImageNode.setAttribute("Name", PathWebp)
        resourceImageNode.setAttribute("UV", uvStr)
        resourceImageNode.setAttribute("UVRotate", uvRotate)
        resourceImageNode.setAttribute("Alpha", alpha)
        resourceImageNode.setAttribute("MaxSize", MaxSize)

        if __Dir is not None:
            resourceImageNode.setAttribute("__Dir", __Dir)
            pass

        if Size is not None:
            resourceImageNode.setAttribute("Size", Size)
            pass

        if Offset is not None:
            resourceImageNode.setAttribute("Offset", Offset)
            pass

        self.setAlreadyInAtlas()
        pass

    def __replaceFileNodeRGB(self, filename, __Dir, uvStr, uvRotate, MaxSize, Size, Offset):
        self.node.setAttribute("Type", "ResourceImageSubstract")

        if self.fileNode is not None:
            self.fileNode.removeFromParent()
            pass

        resourceImageNode = self.node.createChildren("Image")

        PathRGB = FileSystem.setFileExtension(filename, "htf")

        resourceImageNode.setAttribute("Name", PathRGB)
        resourceImageNode.setAttribute("UV", uvStr)
        resourceImageNode.setAttribute("UVRotate", uvRotate)
        resourceImageNode.setAttribute("Alpha", "0")
        resourceImageNode.setAttribute("MaxSize", MaxSize)

        if __Dir is not None:
            resourceImageNode.setAttribute("__Dir", __Dir)
            pass

        if Size is not None:
            resourceImageNode.setAttribute("Size", Size)
            pass

        if Offset is not None:
            resourceImageNode.setAttribute("Offset", Offset)
            pass

        self.setAlreadyInAtlas()
        pass

    def __replaceFileNodeRGBA(self, filename, __Dir, uvStr, uvRotate, MaxSize, Size, Offset):
        self.node.setAttribute("Type", "ResourceImageSubstractRGBAndAlpha")

        if self.fileNode is not None:
            self.fileNode.removeFromParent()
            pass

        resourceImageNode = self.node.createChildren("Image")

        PathRGB = FileSystem.setFileExtension(filename, "htf")
        PathAlpha = FileSystem.setFileExtension(filename, "acf")

        resourceImageNode.setAttribute("NameRGB", PathRGB)
        resourceImageNode.setAttribute("UVRGB", uvStr)
        resourceImageNode.setAttribute("UVRGBRotate", uvRotate)

        resourceImageNode.setAttribute("NameAlpha", PathAlpha)
        resourceImageNode.setAttribute("UVAlpha", uvStr)
        resourceImageNode.setAttribute("UVAlphaRotate", uvRotate)

        resourceImageNode.setAttribute("MaxSize", MaxSize)

        if __Dir is not None:
            resourceImageNode.setAttribute("__Dir", __Dir)
            pass

        if Size is not None:
            resourceImageNode.setAttribute("Size", Size)
            pass

        if Offset is not None:
            resourceImageNode.setAttribute("Offset", Offset)
            pass

        self.setAlreadyInAtlas()
        pass

    def _onPackToAtlas(self, image, atlas):
        uv = image.getUV()

        alpha = "0"
        if self.fileNode.hasAttribute("Alpha"):
            alpha = self.fileNode.getAttribute("Alpha")
            pass
        else:
            alpha = self._ifAlpha(image)
            pass

        MaxSize = "0.0; 0.0"
        if self.fileNode.hasAttribute("MaxSize"):
            MaxSize = self.fileNode.getAttribute("MaxSize")
            pass

        Size = None
        if self.fileNode.hasAttribute("Size"):
            Size = self.fileNode.getAttribute("Size")
            pass

        Offset = None
        if self.fileNode.hasAttribute("Offset"):
            Offset = self.fileNode.getAttribute("Offset")
            pass

        __Dir = None
        if self.fileNode.hasAttribute("__Dir"):
            __Dir = self.fileNode.getAttribute("__Dir")
            pass

        uvStr = self.__makeUV(uv, image.isRotate())
        uvRotate = "1" if image.isRotate() is True else "0"

        project = Environment.getCurrentProject()

        if project.imageConvertMode == Constants.IMAGE_MODE_CONVERT_NO_CONVERT:
            self.__replaceFileNodeNoConvert(atlas.fileName, __Dir, uvStr, uvRotate, MaxSize, Size, Offset, alpha)
            pass
        elif project.imageConvertMode == Constants.IMAGE_MODE_CONVERT_PNG_TO_WEBP:
            self.__replaceFileNodeWebp(atlas.fileName, __Dir, uvStr, uvRotate, MaxSize, Size, Offset, alpha)
            pass
        elif alpha == "0":
            self.__replaceFileNodeRGB(atlas.fileName, __Dir, uvStr, uvRotate, MaxSize, Size, Offset)
            pass
        else:
            self.__replaceFileNodeRGBA(atlas.fileName, __Dir, uvStr, uvRotate, MaxSize, Size, Offset)
            pass
        pass

    def _ifAlpha(self, image):
        img = image.getImagePIL()

        if ToolsBuilderPlugin.uselessalphaImage(img) is True:
            return "0"
            pass

        return "1"
        pass

    def _onPackToAtlasEnd(self, image, atlas):
        atlasPath = atlas.fileName

        if atlasPath not in atlas.getWritenAtlases():
            atlas.addWritenAtlas(atlas.fileName)
            self._addAtlasNode(atlas)
            pass
        pass

    def _addAtlasNode(self, atlas):
        OldName = self.node.getAttribute("Name")

        ResourceATLASName = OldName + "_ATLAS"

        atlas_node = None
        if len(self.includes) != 0:
            atlas_node = self.includes[0].getParent()
        else:
            atlas_node = self.node.getParent()
            pass

        atlasNode = atlas_node.createChildrenFront("Resource")
        atlasNode.setAttribute("Name", ResourceATLASName)
        atlasNode.setAttribute("Type", "ResourceImageDefault")
        atlasNode.setAttribute("Unique", "0")

        atlasFileNode = atlasNode.createChildren("File")
        atlasFileNode.setAttribute("Path", atlas.fileName)
        atlasFileNode.setAttribute("__IsAtlas", "1")
        atlasFileNode.setAttribute("__Dir", atlas.getFileName())
        atlasFileNode.setAttribute("Codec", "pngImage")
        atlasFileNode.setAttribute("NoConvert", "0")

        project = Environment.getCurrentProject()

        if project.imagePremultiply is True:
            atlasFileNode.setAttribute("Premultiply", "1")
            pass

#        bound = atlas.getBound()
#        boundX = bound[0] * atlas.width
#        boundY = bound[1] * atlas.height

        MaxSize = "%d;%d" % (atlas.width, atlas.height)

        atlasFileNode.setAttribute("MaxSize", MaxSize)
        pass

    def getFilePath(self):
        return self.fileNode.getAttribute("Path")
        pass

    def getImage(self):
        path = self.getFilePath()

        if self.fileNode.hasAttribute("__Dir"):
            pathFile = self.fileNode.getAttribute("__Dir")
            pass
        else:
            pathFile = self.fileSystemCursor.getFileSourcePath(path)
            pass

        image = AtlasImagePyBuilder(path=pathFile, onPackCallback=self._onPackToAtlas, onPackCallbackEnd=self._onPackToAtlasEnd)

        return image
        pass
    pass
