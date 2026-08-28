from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.FileSystem import FileSystem
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.Operation.OperationManager import OperationManager
from Builder.Environment import Environment

class ResourceHandlerVideo(ResourceHandler):
    def _onExecute(self):
        if self.workWithFileNodes() is False:
            return False

        return True
        pass

    def convertFFMPEGtoWEBM(self, fileNode):
        project = Environment.getCurrentProject()

        if fileNode.hasAttribute("Converter") and fileNode.getAttribute("Converter") == "ffmpegToWebM":
            path = fileNode.getAttribute("Path")
            pathWEBM = FileSystem.setFileExtension(path, "webm")

            destination = self.fileSystemCursor.getFileDestinationPath(pathWEBM)
            source = self.fileSystemCursor.getFileSourcePath(path)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation('ConvertFFMPEGtoWEBM', SourcePath=source, DestinationPath=destination, Resize=project.videoResize)
                pass

                fileNode.removeAttribute("Converter")
                fileNode.setAttribute("Codec", "ffmpegVideo")
                fileNode.setAttribute("Path", pathWEBM)
                self.setDocumentToRewrite()
            pass
        elif fileNode.hasAttribute("Converter") and fileNode.getAttribute("Converter") == "ffmpegToOGV":
            path = fileNode.getAttribute("Path")
            pathOGV = FileSystem.setFileExtension(path, "ogv")

            destination = self.fileSystemCursor.getFileDestinationPath(pathOGV)
            source = self.fileSystemCursor.getFileSourcePath(path)

            quality = project.videoConvertQuality
            resize = project.videoResize

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertFFMPEGtoOGV", SourcePath=source, DestinationPath=destination, Quality=quality, Resize=resize)
                pass

            fileNode.removeAttribute("Converter")
            fileNode.setAttribute("Codec", "ogvVideo")
            fileNode.setAttribute("Path", pathOGV)
            self.setDocumentToRewrite()
            pass
        elif fileNode.hasAttribute("Converter") and fileNode.getAttribute("Converter") == "ffmpegToOGVA":
            path = fileNode.getAttribute("Path")
            pathOGV = FileSystem.setFileExtension(path, "ogv")

            destination = self.fileSystemCursor.getFileDestinationPath(pathOGV)
            source = self.fileSystemCursor.getFileSourcePath(path)

            quality = project.videoConvertQuality
            resize = project.videoResize

            with OperationManager.runOperationChain() as oc:
                oc.addOperation("ConvertFFMPEGtoOGVA", SourcePath=source, DestinationPath=destination, Quality=quality, Resize=resize)
                pass

            fileNode.removeAttribute("Converter")
            fileNode.setAttribute("Codec", "ogvaVideo")
            fileNode.setAttribute("Path", pathOGV)

            self.setDocumentToRewrite()
            pass
        elif fileNode.hasAttribute("Converter") and fileNode.getAttribute("Converter") == "ffmpegToGVF":
            path = fileNode.getAttribute("Path")
            pathGVF = FileSystem.setFileExtension(path, "gvf")

            destination = self.fileSystemCursor.getFileDestinationPath(pathGVF)
            source = self.fileSystemCursor.getFileSourcePath(path)

            with OperationManager.runOperationChain() as oc:
                oc.addOperation('ConvertFFMPEGtoGVF', SourcePath=source, DestinationPath=destination, Resize=project.videoResize)
                pass

            fileNode.removeAttribute("Converter")
            fileNode.setAttribute("Codec", "gvfVideo")
            fileNode.setAttribute("Path", pathGVF)
            self.setDocumentToRewrite()
            pass
        elif not fileNode.hasAttribute("Converter") and fileNode.hasAttribute("Quality") and fileNode.getAttribute("Quality") != "100":
            path = fileNode.getAttribute("Path")
            codec = fileNode.getAttribute("Codec")

            destination = self.fileSystemCursor.getFileDestinationPath(path)
            source = self.fileSystemCursor.getFileSourcePath(path)

            if codec == "ogvVideo":
                quality = project.videoConvertQuality
                resize = project.videoResize

                with OperationManager.runOperationChain() as oc:
                    oc.addOperation("ConvertFFMPEGtoOGV", SourcePath=source, DestinationPath=destination, Quality=quality, Resize=resize)
                    pass
                pass
            elif codec == "ogvaVideo":
                quality = project.videoConvertQuality
                resize = project.videoResize

                with OperationManager.runOperationChain() as oc:
                    oc.addOperation("ConvertFFMPEGtoOGVA", SourcePath=source, DestinationPath=destination, Quality=quality, Resize=resize)
                    pass
                pass
            else:
                ErrorHandler.error("unsupported codec: %s" % (codec))
                return False
                pass
        else:
            if fileNode.hasAttribute("Converter"):
                ErrorHandler.error("Wrong converter attribute, %s" % (fileNode.getAttribute("Converter")))
                return False
                pass

            path = fileNode.getAttribute("Path")
            extension = FileSystem.getFileExtension(path)

            destination = self.fileSystemCursor.getFileDestinationPath(path)
            source = self.fileSystemCursor.getFileSourcePath(path)

            if extension == "flv":
                with OperationManager.runOperationChain() as oc:
                    oc.addOperation('CopyFile', SourcePath=source, DestinationPath=destination, Doc="ResourceHandlerVideo")
                    oc.addOperation('YamdiOptimize', SourcePath=source, DestinationPath=destination)
                    pass

                return True
                pass

            if project.videoResize is not None:
                with OperationManager.runOperationChain() as oc:
                    oc.addOperation('ResizeVideo', SourcePath=source, DestinationPath=destination, Resize=project.videoResize)
                    pass

                fileNode.setAttribute("Resize", "{0}".format(project.videoResize))
            else:
                self.copyFile(path, path)
                pass
            pass

        return True
        pass

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)

            return False
            pass

        if self.convertFFMPEGtoWEBM(fileNode) is False:
            return False
            pass

        return True
        pass
    pass
