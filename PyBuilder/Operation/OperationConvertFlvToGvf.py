from PyBuilder.Operation.Operation import Operation
from PyBuilder.FileSystem import FileSystem
import struct
import glob
from PIL import Image

from PyBuilder.OSSystem import OSSystem

import ToolsBuilderPlugin

class OperationConvertFlvToGvf(Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.tempDir = params.pop("TempDir")

        self.sourceDir = FileSystem.getDirname(self.sourcePath)
        self.offsets = []
        self.data = b''
        pass

    def _getInfo(self):
        return ("convert %s  to %s" % ( self.sourcePath, self.destinationPath ) )
        pass

    def _onRun(self):
        dirName = FileSystem.getDirname(self.destinationPath)
        if FileSystem.isDirectory(dirName) == False and dirName != '':
            FileSystem.makeDirsRecursive(dirName)
            pass

        self.temp1 = FileSystem.joinAndNormalisePath(self.tempDir, "temp1")
        self.temp2 = FileSystem.joinAndNormalisePath(self.tempDir, "temp2")

        filePngNames = []

        if FileSystem.isDirectory(self.temp1):
            FileSystem.removeDirRecursive(self.temp1)
            pass
        if FileSystem.isDirectory(self.temp2):
            FileSystem.removeDirRecursive(self.temp2)
            pass
        FileSystem.makeDirsRecursiveIfNotExist(self.temp1)
        FileSystem.makeDirsRecursiveIfNotExist(self.temp2)

        self._parseToPng()

        currentPath = FileSystem.joinAndNormalisePath(self.temp1, "*.png")
        for file in glob.glob(currentPath):
            filePngNames.append(file)
            pass
        if ToolsBuilderPlugin.isAlphaInImageFile(filePngNames[0]) is True:
            self.alpha = 1
            pass
        else:
            self.alpha = 0
            pass
        self.lenFiles = len(filePngNames)
        image = Image.open(filePngNames[0])
        self.size = image.size

        for fileName in filePngNames:
            self._pngToWepb(fileName)
            pass

        currentPath = FileSystem.joinAndNormalisePath(self.temp2, "*.webp")
        for fileName in glob.glob(currentPath):
            self._getData(fileName)
            pass

        duration = self.getVideoDuration(self.sourcePath)
        self.fps = self.lenFiles / duration

        self.appendOffset()

        self._writeToFile()

        return True
        pass
    pass

    def appendOffset(self):
        offset = (self.lenFiles+1) * 4 + 20 + len(self.data)
        self.offsets.append(offset)
        pass

    def _parseToPng(self):
        tempFiles = FileSystem.joinAndNormalisePath(self.temp1, "image%04d.png")
        if OSSystem.tool("ffmpeg", "-i", self.sourcePath, tempFiles) is False:
            return False
            pass

        return True
        pass

    def _pngToWepb(self, fileName):
        baseName = FileSystem.getBasename(fileName)
        newFileName = FileSystem.setFileExtension(baseName, "webp")
        newFilePath = FileSystem.joinAndNormalisePath(self.temp2, newFileName)

        if OSSystem.tool("cwebp", "-quiet", "-q", "100", fileName, "-o", newFilePath) is False:
            return False
            pass

        return True
        pass

    def _getData(self, fileName):
        f = open(fileName, "rb")
        dataBlock = f.read()
        f.close()
        self.appendOffset()
        self.data += dataBlock
        pass

    def _writeToFile(self):
        with open(self.destinationPath, "wb") as f_out:
            f_out.write(struct.pack("i", (self.lenFiles)))
            f_out.write(struct.pack("i", (int(self.fps))))
            f_out.write(struct.pack("i", (self.size[0])))
            f_out.write(struct.pack("i", (self.size[1])))
            f_out.write(struct.pack("i", self.alpha))
            for offset in self.offsets:
                f_out.write(struct.pack("i", offset))
                pass
            f_out.write(self.data)
            pass
        return True
        pass


    def getVideoDuration(self, src_file):
        returncode, output = OSSystem.process_tool(
            "ffprobe",
            ("-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", src_file),
        )

        if returncode != 0:
            return 0
            pass

        return float(output.strip())
        pass
