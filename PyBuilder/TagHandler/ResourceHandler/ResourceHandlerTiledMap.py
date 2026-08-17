import os.path

from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler


class ResourceHandlerTiledMap(ResourceHandler):
    @staticmethod
    def _normaliseTiledPath(path):
        return path.replace("\\", os.sep).replace("/", os.sep)

    def _onExecute(self):
        return self.workWithFileNodes()

    def _workWithFileNode(self, fileNode):
        if fileNode.hasAttribute("Path") is False:
            ErrorHandler.warning("%s :: tag File must have path attribute", self)
            return False

        path = fileNode.getAttribute("Path")

        if FileSystem.getFileExtension(path) not in ("json", "tmj"):
            ErrorHandler.warning("Tiled map Path must use .json or .tmj: %s", path)
            return False

        if fileNode.hasAttribute("__Dir"):
            source = fileNode.getAttribute("__Dir")
        else:
            source = self.fileSystemCursor.getFileSourcePath(path)

        if FileSystem.isAccess(source) is False:
            if fileNode.hasAttribute("NoExist") and fileNode.getAttribute("NoExist") == "1":
                return True

            ErrorHandler.warning("Tiled map source does not exist %s", source)
            return False

        mapData = FileSystem.jsonFileLoadContents(source)

        if isinstance(mapData, dict) is False:
            ErrorHandler.warning("invalid Tiled map JSON %s", source)
            return False

        tilesets = mapData.get("tilesets", [])

        if isinstance(tilesets, list) is False:
            ErrorHandler.warning("invalid Tiled map tilesets %s", source)
            return False

        externalFiles = []
        externalPaths = set()

        for tileset in tilesets:
            if isinstance(tileset, dict) is False:
                ErrorHandler.warning("invalid Tiled map tileset %s", source)
                return False

            tilesetSource = tileset.get("source")

            if tilesetSource is None:
                continue

            if isinstance(tilesetSource, str) is False:
                ErrorHandler.warning("invalid Tiled external tileset source %s", source)
                return False

            tilesetSource = self._normaliseTiledPath(tilesetSource)
            externalPath = FileSystem.joinAndNormalisePath(FileSystem.getDirname(path), tilesetSource)

            if os.path.isabs(externalPath) or externalPath == ".." or externalPath.startswith(".." + os.sep):
                ErrorHandler.warning("Tiled external tileset escapes resources %s", tilesetSource)
                return False

            if FileSystem.getFileExtension(externalPath) not in ("json", "tsj"):
                ErrorHandler.warning("Tiled external tileset must use .json or .tsj: %s", tilesetSource)
                return False

            externalSource = FileSystem.joinAndNormalisePath(FileSystem.getDirname(source), tilesetSource)

            if FileSystem.isAccess(externalSource) is False:
                ErrorHandler.warning("Tiled external tileset does not exist %s", externalSource)
                return False

            externalDestination = self.fileSystemCursor.getFileDestinationPath(externalPath)

            if externalDestination in externalPaths:
                continue

            externalPaths.add(externalDestination)
            externalFiles.append((externalSource, externalDestination))

        self.copyFile(source, self.fileSystemCursor.getFileDestinationPath(path))

        for externalSource, externalDestination in externalFiles:
            self.copyFile(externalSource, externalDestination)

        return True
