__author__ = 'human88998999877'
from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Operation.OperationManager import OperationManager
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler

from PyBuilder.OSSystem import OSSystem

class PyBuilderActionChangeIniConfig(PyBuilderAction):
    def _onInitialise(self):
        pass

    def _onRun(self):
        for PackName in self.project.packNames:
            section = self.project.getPackageIni(PackName)

            if "Path" in section:
                Path = section["Path"]

                if FileSystem.getFileExtension(section["Path"]) == "":
                    FolderPackagesIni = FileSystem.splitPath(self.project.pathToPackagesIni)[0]
                    NormalizePath = FileSystem.joinAndNormalisePath(FolderPackagesIni, Path)
                    newPath = FileSystem.getRelPath(self.project.sourceDir, NormalizePath)
                    newPath = FileSystem.addFolderBackslash(newPath)
                    newPath = newPath.replace("\\", "/")

                    section["Path"] = FileSystem.addFolderBackslash(newPath)
                else:
                    section["Path"] = FileSystem.getBasename(Path)
                    pass
                pass
            pass

        pass

    def _onFinalise(self):
        #configs
        if self.project.pathToConfigsIni is not None:
            baseName = FileSystem.getBasename(self.project.pathToConfigsIni)
            newIniPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite configs ini %s" % newIniPath)
            self.project.configsIni.write(newIniPath)
            pass

        #credentials
        if self.project.pathToCredentialsIni is not None:
            baseName = FileSystem.getBasename(self.project.pathToCredentialsIni)
            newIniPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite credentials ini %s" % newIniPath)
            self.project.credentialsIni.write(newIniPath)

            secureValue = self.project.secureValue or "0123456789A"

            if OSSystem.tool("Ravinggen", "--in", self.project.pathToCredentialsJson, "--out", newJsonPath, "--secure", secureValue) is False:
                return False
                pass
            pass

        #packages
        if self.project.pathToPackagesIni is not None:
            baseName = FileSystem.getBasename(self.project.pathToPackagesIni)
            newIniPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite packages ini %s" % newIniPath)
            self.project.packagesIni.write(newIniPath)
            pass

        #settings
        if self.project.pathToSettingsIni is not None:
            baseName = FileSystem.getBasename(self.project.pathToSettingsIni)
            newIniPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite packages ini %s" % newIniPath)
            self.project.settingsIni.write(newIniPath)
            pass

        #Application
        iniName = FileSystem.getBasename(self.project.pathToApplicationIni)
        newIniPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, iniName)

        #Set new path to root of the project
        if self.project.pathToConfigsIni is not None:
            self.project.applicationConfig["Configs"]["Path"] = FileSystem.getBasename(self.project.pathToConfigsIni)
            pass

        if self.project.pathToCredentialsIni is not None:
            self.project.applicationConfig["Credentials"]["Path"] = FileSystem.getBasename(self.project.pathToCredentialsIni)
            pass

        if self.project.pathToPackagesIni is not None:
            self.project.applicationConfig["Packages"]["Path"] = FileSystem.getBasename(self.project.pathToPackagesIni)
            pass

        if self.project.pathToSettingsIni is not None:
            self.project.applicationConfig["Settings"]["Path"] = FileSystem.getBasename(self.project.pathToSettingsIni)

            for Path in self.project.settingPaths:
                SourcePath = FileSystem.joinAndNormalisePath(self.project.sourceDir, Path)
                DestinationPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, Path)

                FileSystem.copyFile(SourcePath, DestinationPath)
                pass
            pass

        ErrorHandler.importantMessage("Rewrite application ini %s"%newIniPath)
        self.project.applicationConfig.write(newIniPath)
        pass
    pass
