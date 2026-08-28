from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.FileSystem import FileSystem

from Builder import Tools

class ResourceHandlerImageConvert(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def _workWithFileNode(self, fileNode):
        filename = fileNode.getAttribute("Path")

        if fileNode.hasAttribute("__Dir"):
            fullPath = fileNode.getAttribute("__Dir")
            pass
        else:
            fullPath = self.fileSystemCursor.getFileSourcePath(filename)
            pass

        IsAtlas = False
        if fileNode.hasAttribute("__IsAtlas"):
            if fileNode.getAttribute("__IsAtlas") == "1":
                IsAtlas = True
                pass
            pass

        if fileNode.hasAttribute("NoExist"):
            if fileNode.getAttribute("NoExist") == "1":
                if FileSystem.isAccess(fullPath) is False:
                    return
                    pass
                pass
            pass

        NoAtlas = False
        if fileNode.hasAttribute("NoAtlas"):
            if fileNode.getAttribute("NoAtlas") == "1":
                NoAtlas = True
                pass
            pass

        NoConvert = False
        if fileNode.hasAttribute("NoConvert"):
            if fileNode.getAttribute("NoConvert") == "1":
                NoConvert = True
                pass
            pass

        MaxSize = fileNode.getAttribute("MaxSize")

        MaxSizeX, MaxSizeY = map(int, MaxSize.replace(";", " ").split())

        def __ispow2(n):
            return n != 0 and (n & (n - 1)) == 0

        if __ispow2(MaxSizeX) is True and __ispow2(MaxSizeY) is False and MaxSizeX > 256 and MaxSizeY > 256:
            NoAtlas = True
            pass

        if Tools.isAlphaInImageFile(fullPath) is True:
            fileNode.setAttribute("Alpha", "1")
            pass
        else:
            fileNode.setAttribute("Alpha", "0")
            pass

        if NoConvert is True:
            PathExt = FileSystem.getFileExtension(filename)

            if PathExt == "png" or PathExt == "PNG":
                fileNode.setAttribute("Codec", "pngImage")
                pass
            elif PathExt == "jpg" or PathExt == "JPG" or PathExt == "jpeg" or PathExt == "JPEG":
                fileNode.setAttribute("Codec", "jpegImage")
                pass

            destinationFull = self.fileSystemCursor.getFileDestinationPath(filename)

            self.copyFile(fullPath, destinationFull)
            pass
        else:
            if self._process(fullPath, fileNode, NoAtlas, IsAtlas) is False:
                return False
                pass
            pass

        self.setDocumentToRewrite()

        return True
        pass

    def _process(self, fullPath, fileNode, NoAtlas, IsAtlas):
        if Tools.isUselessAlphaInImageFile(fullPath) is False:
            if self._proccesRGBA(fullPath, fileNode, NoAtlas, IsAtlas) is False:
                return False
                pass
            pass
        else:
            if self._proccesRGB(fullPath, fileNode, NoAtlas, IsAtlas) is False:
                return False
                pass
            pass

        return True
        pass
    pass
