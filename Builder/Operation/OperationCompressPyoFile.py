from Builder.Operation.Operation import Operation
from Builder.FileSystem import FileSystem
import zlib
import struct

class OperationCompressPyoFile (Operation):
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

        fCompressed = zlib.compress(data)

        sizePyo = len(data)
        sizePyoCompress = len(fCompressed)

        with open(self.destinationPath, "wb") as f_out:
            f_out.write(struct.pack("i", 0))
            f_out.write(struct.pack("i", sizePyo))
            f_out.write(struct.pack("i", sizePyoCompress))
            f_out.write(fCompressed)
            pass

        FileSystem.removeFile(self.sourcePath)

        return True
        pass
    pass
