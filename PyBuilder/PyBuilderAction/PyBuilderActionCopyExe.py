__author__ = 'human88998999877'
from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder import Constants


class PyBuilderActionCopyExe(PyBuilderAction):
    def _onRun(self):
        ErrorHandler.importantMessage("Copy exe files from %s to %s " % (self.project.pathToSourceExe, self.project.pathToDestinationExe) )

        exePath = FileSystem.joinAndNormalisePath(self.project.destinationDir, self.project.newExeFileName)
        oldExePath = FileSystem.joinAndNormalisePath(self.project.destinationDir, self.project.oldExeFileName)
        def copyFileHandler(fileSource,fileDestiny):
            with OperationManager.runOperationChain() as oc:
                oc.addOperation("CopyFile", SourcePath = fileSource, DestinationPath = fileDestiny, Doc="PyBuilderActionCopyExe")
                pass
            pass

        with OperationManager.runOperationChain() as oc:
            oc.addOperation("CopyDirRecursive",
                            SourcePath = self.project.pathToSourceExe,
                            DestinationPath = self.project.pathToDestinationExe,
                            IgnoredPatterns = ".svn",
                            CopyFileCallback = copyFileHandler)

            oc.addOperation("RenameFile", OldName = oldExePath, NewName = exePath)

            oc.addOperation("SetExeVersionInfo",
                            Version = Constants.EXE_FILE_VERSION,
                            CompanyInfo = Constants.EXE_FILE_COMPANY,
                            Description = self.project.exeFileDescription,
                            SourcePath = exePath)

            if self.project.pathToIconGroup != None:
                oc.addOperation("ChangeIcons",
                                IconsName = Constants.ICONS_NAME,
                                IconsPath = self.project.pathToIconGroup,
                                SourcePath = exePath)
                pass

            pass
        pass
    pass
