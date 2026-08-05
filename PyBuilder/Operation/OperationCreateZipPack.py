from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Operation.Operation import Operation

from zipfile import ZipFile, ZIP_STORED

import os

class OperationCreateZipPack(Operation):
    def __init__(self):
        super(OperationCreateZipPack, self).__init__()
        pass

    def _getInfo(self):
        return (" source  %s \n\r destiny %s " %  (self.sourcePath, self.destinationPath  ) )
        pass

    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.ignoredList = params.pop("IgnoredList", [])
        self.splitSize = params.pop("SplitSize", -1)
        pass

    def foreachDirectory(self, directoryName, cb):
        for root, dirs, files in os.walk(directoryName):
            zipRoot = root.replace(directoryName, "")
            for name in files:
                zipFileName = os.path.join(zipRoot, name)
                filePath = os.path.join(root, name)
                fileName, fileExt = os.path.splitext(filePath)
                isSkip = False
                for ignored in self.ignoredList:
                    if fileExt.find(ignored) != -1:
                        isSkip = True
                        break
                        pass
                    pass

                if isSkip is True:
                    continue
                    pass

                fileSize = os.path.getsize(filePath)

                cb(zipFileName, filePath, fileSize)
                pass
            pass
        pass

    def calcTotalSize(self, directoryName):
        totalsize = 0

        def __calcSize(zipFileName, fileName, fileSize):
            nonlocal totalsize

            totalsize += fileSize
            pass

        self.foreachDirectory(directoryName, __calcSize)

        return totalsize
        pass

    def packDirToZip(self, zipName, directoryName):
        totalsize = self.calcTotalSize(directoryName)
        if self.splitSize == -1 or totalsize <= self.splitSize:
            zipFile = ZipFile(zipName, mode='w', compression=ZIP_STORED)

            def __writeZip(zipFileName, fileName, fileSize):
                nonlocal zipFile

                zipFile.write(fileName, compress_type=ZIP_STORED, arcname=zipFileName)
                pass

            self.foreachDirectory(directoryName, __writeZip)
            return
            pass

        zipNameBody, zipNameExt = os.path.splitext(zipName)

        enumerator = 0
        totalsize = 0
        zipFiles = {}

        def __getZipFile(fileSize):
            nonlocal enumerator
            nonlocal totalsize
            nonlocal zipFiles

            if fileSize > self.splitSize:
                return None
                pass

            if totalsize + fileSize > self.splitSize:
                enumerator += 1
                totalsize = 0
                pass

            totalsize += fileSize

            zipFile = zipFiles.get(enumerator, None)

            if zipFile is None:
                zipChunkName = self.project.CreatePacksFormat % (zipNameBody, enumerator, zipNameExt)

                zipFile = ZipFile(zipChunkName, mode='w', compression=ZIP_STORED)

                zipFiles[enumerator] = zipFile

                return zipFile
                pass

            return zipFile
            pass

        def __writeZip(zipFileName, fileName, fileSize):
            zipFile = __getZipFile(fileSize)
            zipFile.write(fileName, compress_type=ZIP_STORED, arcname=zipFileName)
            pass

        self.foreachDirectory(directoryName, __writeZip)

        sectionName = FileSystem.getBasename(directoryName)
        self.project.packagesJson.rewritePathsInSection(sectionName, self.project.CreatePacksFormat)
        pass
    pass

    def _onRun(self):
        self.packDirToZip(self.destinationPath, self.sourcePath)
        pass
    pass
