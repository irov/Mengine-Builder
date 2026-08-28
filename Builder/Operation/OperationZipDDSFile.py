from Builder.Operation.Operation import Operation
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
import zlib
import struct

class OperationZipDDSFile (Operation):
    def _onParams( self, params ):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        pass

    def _getInfo(self):
        return ("compress %s  to %s" % ( self.sourcePath, self.destinationPath ) )
        pass

    def _onRun(self):
        f = open(self.sourcePath, "rb")

        data = f.read()
        f.close()

        dataHeader = data[:128]
        dataBody = data[128:]

        dataBodyCompressed = zlib.compress(dataBody)

        sizeUncompressed = len(data)
        sizeCompressed = len(dataBodyCompressed)

        with open(self.destinationPath, "wb") as f_out:
            f_out.write(struct.pack("i", sizeUncompressed))
            f_out.write(struct.pack("i", sizeCompressed))
            f_out.write(dataHeader)
            f_out.write(dataBodyCompressed)
            pass

        FileSystem.removeFile(self.sourcePath)

        return True
        pass
    pass
