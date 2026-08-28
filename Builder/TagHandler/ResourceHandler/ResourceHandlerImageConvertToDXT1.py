from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvert import ResourceHandlerImageConvert
from Builder.FileSystem import FileSystem
from Builder.Operation.OperationManager import OperationManager

from Builder.Environment import Environment

from Builder import Tools

#attach this to  "ResourceImageDefault" or checkAttributeType == "ResourceImageInAtlasCombineRGBAndAlpha"
class ResourceHandlerImageConvertToDXT1(ResourceHandlerImageConvert):
    def makeSplitPathRGB(self, filename, mode, ext):
        parts = FileSystem.splitByExtension(filename)
        splitPath = "%s_%s.%s"%(parts[0], mode, ext)

        project = Environment.getCurrentProject()
        temp = FileSystem.joinAndNormalisePath(project.logDir, "pngSplit")
        tempDir = FileSystem.joinAndNormalisePath(temp, FileSystem.getDirname(splitPath))
        FileSystem.makeDirsRecursiveIfNotExist(tempDir)
        newPath = FileSystem.joinAndNormalisePath(temp, splitPath)

        return newPath
        pass

    def _proccesRGBA(self, fullPath, fileNode, NoAtlas, IsAtlas):
        filename = fileNode.getAttribute("Path")

        PathRGB = FileSystem.setFileExtension(filename, "htf")
        PathAlpha = FileSystem.setFileExtension(filename, "acf")

        if NoAtlas is True:
            OldName = self.node.getAttribute("Name")

            ResourceRGBName = OldName + "_RGB"
            ResourceRGBAlpha = OldName + "_ALPHA"

            self.node.setAttribute("Type", "ResourceImageSubstractRGBAndAlpha")

            imageNode = self.node.createChildren("Image")
            imageNode.setAttribute("NameRGB", ResourceRGBName)
            imageNode.setAttribute("UVRGB", "0.0;0.0;1.0;0.0;1.0;1.0;0.0;1.0")
            imageNode.setAttribute("NameAlpha", ResourceRGBAlpha)
            imageNode.setAttribute("UVAlpha", "0.0;0.0;1.0;0.0;1.0;1.0;0.0;1.0")
            imageNode.setAttribute("MaxSize", fileNode.getAttribute("MaxSize"))

            rgbNode = self.node.getParent().createChildren("Resource", self.node)
            rgbNode.setAttribute("Name", ResourceRGBName)
            rgbNode.setAttribute("Type", "ResourceImageDefault")

            rgbFileNode = rgbNode.createChildren("File")
            rgbFileNode.setAttribute("Path", PathRGB)
            rgbFileNode.setAttribute("Codec", "htfImage")
            rgbFileNode.setAttribute("MaxSize", fileNode.getAttribute("MaxSize"))
            rgbFileNode.setAttribute("NoConvert", "0")

            if self.node.hasAttribute("Unique") is True:
                OldUnique = self.node.getAttribute("Unique")
                rgbNode.setAttribute("Unique", OldUnique)
                pass
            pass

            alphaNode = self.node.getParent().createChildren("Resource", self.node)
            alphaNode.setAttribute("Name", ResourceRGBAlpha)
            alphaNode.setAttribute("Type", "ResourceImageDefault")

            alphaFileNode = alphaNode.createChildren("File")
            alphaFileNode.setAttribute("Path", PathAlpha)
            alphaFileNode.setAttribute("Codec", "acfImage")
            alphaFileNode.setAttribute("MaxSize", fileNode.getAttribute("MaxSize"))
            alphaFileNode.setAttribute("NoConvert", "0")

            if self.node.hasAttribute("Unique") is True:
                OldUnique = self.node.getAttribute("Unique")
                alphaNode.setAttribute("Unique", OldUnique)
                pass
            pass
        else:
            self.node.setAttribute("Name", PathRGB)

            fileNode.setAttribute("Codec", "htfImage")
            fileNode.setAttribute("Path", PathRGB)
            fileNode.setAttribute("NoConvert", "0")

            alphaNode = self.node.getParent().createChildren("Resource", self.node)
            alphaNode.setAttribute("Name", PathAlpha)
            alphaNode.setAttribute("Type", "ResourceImageDefault")

            alphaFileNode = alphaNode.createChildren("File")
            alphaFileNode.setAttribute("Path", PathAlpha)
            alphaFileNode.setAttribute("Codec", "acfImage")
            alphaFileNode.setAttribute("MaxSize", fileNode.getAttribute("MaxSize"))
            alphaFileNode.setAttribute("NoConvert", "0")
            pass

        SplitPathRGB = self.makeSplitPathRGB(fullPath, "rgb", "png")
        SplitPathAlpha = self.makeSplitPathRGB(fullPath, "alpha", "png")
        SplitPathDDS = self.makeSplitPathRGB(fullPath, "dds", "dds")

        fullPathSource = self.fileSystemCursor.getFileSourcePath(fullPath)
        fullPathRGB = self.fileSystemCursor.getFileDestinationPath(PathRGB)
        fullPathAlpha = self.fileSystemCursor.getFileDestinationPath(PathAlpha)

        project = Environment.getCurrentProject()

        imageConvertQuality = project.imageConvertQuality

        with OperationManager.runOperationChain() as oc:
            oc.addOperation( "SplitImageOnRGBAndAlpha"
                             , SourcePath = fullPathSource
                             , DestinationPathRGB = SplitPathRGB
                             , DestinationPathAlpha = SplitPathAlpha
                             , Quality = imageConvertQuality
                             , FormatRGB = "PNG"
                             , FormatAlpha = "PNG" )
            oc.addOperation( "ConvertImageToDDS"
                             , SourcePath = SplitPathRGB
                             , DestinationPath = SplitPathDDS
                             , Quality = imageConvertQuality
                             , Format = "dxt1" )
            oc.addOperation( "ConvertImageToACF"
                             , SourcePath = SplitPathAlpha
                             , DestinationPath = fullPathAlpha
                             , Quality = imageConvertQuality )
            oc.addOperation( "ConvertImageToHTF"
                             , SourcePath = SplitPathDDS
                             , DestinationPath = fullPathRGB
                             , Quality = imageConvertQuality
                             , Codec = "dds2htf" )
            pass

        if oc.isSuccess() is False:
            return False
            pass

        return True
        pass

    def _proccesRGB(self, fullPath, fileNode, NoAtlas, IsAtlas):
        if NoAtlas is True:
            pass
        else:
            OldName = self.node.getAttribute("Name")

            ResourceRGBName = OldName + "_RGB"

            self.node.setAttribute("Name", ResourceRGBName)
            pass

        filename = fileNode.getAttribute("Path")

        PathRGB = FileSystem.setFileExtension(filename, "htf")

        fileNode.setAttribute("Alpha", "0")
        fileNode.setAttribute("Codec", "htfImage")
        fileNode.setAttribute("Path" , PathRGB)

        pathDDS = self.makeSplitPathRGB(fullPath, "dds", "dds")

        destinationFull = self.fileSystemCursor.getFileDestinationPath(PathRGB)

        project = Environment.getCurrentProject()

        imageConvertQuality = project.imageConvertQuality

        with OperationManager.runOperationChain() as oc:
            oc.addOperation( "ConvertImageToDDS"
                             , SourcePath = fullPath
                             , DestinationPath = pathDDS
                             , Quality = imageConvertQuality
                             , Format = "dxt1" )
            oc.addOperation("ConvertImageToHTF"
                            , SourcePath = pathDDS
                            , DestinationPath = destinationFull
                            , Quality = imageConvertQuality
                            , Codec = "dds2htf" )
            pass

        if oc.isSuccess() is False:
            return False
            pass

        return True
        pass
    pass
