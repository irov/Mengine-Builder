from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvert import ResourceHandlerImageConvert
from Builder.FileSystem import FileSystem
from Builder.Operation.OperationManager import OperationManager

from Builder.Environment import Environment

from Builder import Tools

class ResourceHandlerImageConvertToWEBPAndETC1(ResourceHandlerImageConvert):
    def _proccesWEBP(self, fullPath, fileNode, NoAtlas, IsAtlas, Alpha):
        project = Environment.getCurrentProject()

        filename = fileNode.getAttribute("Path")

        PathWEBP = FileSystem.setFileExtension(filename, "webp")

        MakeAtlas = project.isMakeAtlas is True and NoAtlas is False and IsAtlas is True

        if MakeAtlas is True:
            self.node.setAttribute("Name", PathWEBP)
            pass

        fileNode.setAttribute("Codec", "webpImage")
        fileNode.setAttribute("Path", PathWEBP)

        destinationFull = self.fileSystemCursor.getFileDestinationPath(PathWEBP)

        imageConvertQuality = project.imageConvertQuality

        if self.pool.imageQuality is not None:
            imageConvertQuality = int(self.pool.imageQuality)
            pass

        with OperationManager.runOperationChain() as oc:
            oc.addOperation('ConvertImageToWEBP'
                , SourcePath=fullPath
                , DestinationPath=destinationFull
                , Quality=imageConvertQuality
                , Trim=False
                , NoAlpha=not Alpha
            )
            pass

        if oc.isSuccess() is False:
            return False
            pass

        return True
        pass

    def _proccesETC1(self, fullPath, fileNode, NoAtlas, IsAtlas):
        filename = fileNode.getAttribute("Path")

        PathRGB = FileSystem.setFileExtension(filename, "htf")

        fileNode.setAttribute("Alpha", "0")
        fileNode.setAttribute("Codec", "htfImage")
        fileNode.setAttribute("Path", PathRGB)

        PathPVR = FileSystem.setFileExtension(filename, "pvr")

        destinationFull = self.fileSystemCursor.getFileDestinationPath(PathRGB)
        pvrFull = self.fileSystemCursor.getFileTempPath("pvr", PathPVR)

        project = Environment.getCurrentProject()

        imageConvertQuality = project.imageConvertQuality

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("ConvertImageToPVR"
                , SourcePath=fullPath
                , DestinationPath=pvrFull
                , Quality=imageConvertQuality
                , Format="ETC1")
            oc.addOperation("ConvertImageToHTF"
                , SourcePath=pvrFull
                , DestinationPath=destinationFull
                , Quality=imageConvertQuality
                , Codec="pvr2htf")
            pass

        if oc.isSuccess() is False:
            return False
            pass

        return True
        pass

    def _process(self, fullPath, fileNode, NoAtlas, IsAtlas):
        if Tools.isUselessAlphaInImageFile(fullPath) is False:
            if self._proccesWEBP(fullPath, fileNode, NoAtlas, IsAtlas, True) is False:
                return False
                pass
            pass
        else:
            if Tools.isPow2SquadImageFile(fullPath) is True:
                if self._proccesETC1(fullPath, fileNode, NoAtlas, IsAtlas) is False:
                    return False
                    pass
                pass
            else:
                if self._proccesWEBP(fullPath, fileNode, NoAtlas, IsAtlas, False) is False:
                    return False
                    pass
                pass
            pass

        return True
        pass
    pass
