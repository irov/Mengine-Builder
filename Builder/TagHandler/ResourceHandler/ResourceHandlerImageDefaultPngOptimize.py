from pathlib import Path

from Builder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler
from Builder.Operation.OperationManager import OperationManager


class ResourceHandlerImageDefaultPngOptimize(ResourceHandler):
    def _onExecute(self):
        return self.workWithFileNodes()

    def _workWithFileNode(self, fileNode):
        if not fileNode.hasAttribute("Path"):
            raise ValueError("Resource image File must have a Path")
        # Premultiply describes input pixels, not a conversion request.
        # Alpha spreading also skips PMA: RGB must remain zero at A=0.
        if fileNode.hasAttribute("Premultiply") and fileNode.getAttribute("Premultiply").lower() in ("1", "true"):
            return True
        path = fileNode.getAttribute("Path")
        source = fileNode.getAttribute("__Dir") if fileNode.hasAttribute("__Dir") else self.fileSystemCursor.getFileSourcePath(path)
        if fileNode.hasAttribute("NoExist") and fileNode.getAttribute("NoExist") == "1" and not Path(source).is_file():
            return True
        if Path(source).suffix.lower() != ".png":
            return True
        premultiply = self.project.imagePremultiply is True
        destination = self.project.pngOptimizer.output_path(source, premultiply)
        with OperationManager.runOperationChain() as operations:
            operations.addOperation("AliasSafetyPngOptimize", SourcePath=source,
                                    DestinationPath=destination, Premultiply=premultiply)
        if operations.isSuccess() is False:
            return False
        # Export transformed pixels at the original package-relative path.
        # __Dir redirects copying to the temporary result without touching art.
        fileNode.setAttribute("__Dir", destination)
        fileNode.setAttribute("Codec", "pngImage")
        # AlphaSpreading's PNG reader normalizes RGB/palette inputs to RGBA.
        fileNode.setAttribute("Alpha", "1")
        if premultiply:
            fileNode.setAttribute("Premultiply", "1")
        # Only the in-memory graph changes. BuildResources publishes it after
        # the complete preprocessing queue has succeeded.
        self.setDocumentToRewrite()
        return True
