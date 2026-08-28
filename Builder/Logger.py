from Builder.FileSystem import FileSystem
from Builder.Error.Error import BuilderError
import datetime

class Logger:
    def __init__(self):
        self.file = None
        self.fileName = None

        self.pathToLogs = None
        pass

    def getFileName(self):
        return self.fileName
        pass

    def getPathToLogs(self):
        return self.pathToLogs
        pass

    def initialise(self, pathToLogs):
        self.pathToLogs = pathToLogs

        try:
            t = datetime.datetime.today()
            name = t.strftime("%Y_%m_%d_%H_%M")
            fileName = name + ".txt"
            filePath = FileSystem.joinPath(self.pathToLogs, fileName)

            self.file = open(filePath,'w+')
            self.fileName = fileName
            pass
        except BaseException as e:
            raise BuilderError(e)
            pass
        pass

    def write(self,data):
        self.file.write(data+"\n")
        self.file.flush()
        pass

    def finalise(self):
        if self.file is None:
            return
            pass

        self.file.close()
        pass
    pass
