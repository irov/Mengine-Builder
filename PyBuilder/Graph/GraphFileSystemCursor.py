from PyBuilder.FileSystem import FileSystem

class GraphFileSystemCursor(object):
    def __init__(self, project, exportDir, sourceDirName, destinationDirName):
        self.project = project
        self.exportDir = exportDir
        self.sourceDir = sourceDirName
        self.destinationDir = destinationDirName
        pass

    def __repr__(self):
        return "GraphFileSystemCursor :: source - %s destination %s" % (self.sourceDir, self.destinationDir)
        pass

    def isValid(self):
        if FileSystem.isDirectory(self.sourceDir) is False:
            return False
            pass

        return True
        pass

    def getSourceDir(self):
        return self.sourceDir
        pass

    def getDestinationDir(self):
        return self.destinationDir
        pass

    def getFileSourcePath(self, sourceRelativePath):
        fileName = FileSystem.joinAndNormalisePath(self.sourceDir, sourceRelativePath)
        return fileName
        pass

    def getFileExportPath(self, sourceRelativePath):
        fileName = FileSystem.joinAndNormalisePath(self.exportDir, sourceRelativePath)
        return fileName
        pass

    def getFileTempPath(self, temp, sourceRelativePath):
        tmpLogDir = FileSystem.joinAndNormalisePath(self.project.logDir, temp)
        fileName = FileSystem.joinAndNormalisePath(tmpLogDir, sourceRelativePath)
        return fileName
        pass

    def getFileDestinationPath(self, sourceRelativePath):
        fileName = FileSystem.joinAndNormalisePath(self.destinationDir, sourceRelativePath)
        return fileName
        pass

    def getBranch(self, path):
        newPathSource = FileSystem.joinPath(self.sourceDir, path)
        newPathDestination = FileSystem.joinPath(self.destinationDir, path)
        branch = GraphFileSystemCursor(self.project, self.exportDir, newPathSource, newPathDestination)
        return branch
        pass
    pass
