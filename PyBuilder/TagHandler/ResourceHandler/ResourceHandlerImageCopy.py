from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from PyBuilder.FileSystem import FileSystem

from PyBuilder.Environment import Environment

import ToolsBuilderPlugin

class ResourceHandlerImageCopy(ResourceHandler):
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

        if ToolsBuilderPlugin.isAlphaInImageFile(fullPath) is True:
            self.node.setAttribute("Alpha", str(1))
            pass
        else:
            self.node.setAttribute("Alpha", str(0))
            pass

        if NoConvert is True:
            PathExt = FileSystem.getFileExtension(filename)

            if PathExt.lower() == "png":
                fileNode.setAttribute("Codec", "pngImage")
                pass
            elif PathExt.lower() == "jpg" or PathExt.lower() == "jpeg":
                fileNode.setAttribute("Codec", "jpegImage")
                pass

            destinationFull = self.fileSystemCursor.getFileDestinationPath(filename)

            self.copyFile(fullPath, destinationFull)
            pass
        else:
            project = Environment.getCurrentProject()

            if project.isMakeAtlas is True and NoAtlas is False and IsAtlas is True:
                self.node.setAttribute("Name", filename)
                pass

            PathExt = FileSystem.getFileExtension(filename)

            if PathExt.lower() == "png":
                fileNode.setAttribute("Codec", "pngImage")
                pass
            elif PathExt.lower() == "jpg" or PathExt.lower() == "jpeg":
                fileNode.setAttribute("Codec", "jpegImage")
                pass

            destinationFull = self.fileSystemCursor.getFileDestinationPath(filename)

            self.copyFile(fullPath, destinationFull)
            pass

        self.setDocumentToRewrite()

        return True
        pass
    pass
