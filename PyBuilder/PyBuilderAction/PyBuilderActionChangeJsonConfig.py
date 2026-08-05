__author__ = 'human88998999877'
from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Error.ErrorHandler import ErrorHandler

from PyBuilder.OSSystem import OSSystem

class PyBuilderActionChangeJsonConfig(PyBuilderAction):
    def _onInitialise(self):
        pass

    def _onRun(self):
        for PackName in self.project.packNames:
            section = self.project.getPackageJson(PackName)

            if "Path" in section:
                Path = section["Path"]

                if FileSystem.getFileExtension(section["Path"]) == "":
                    FolderPackagesJson, fileName = FileSystem.splitPath(self.project.pathToPackagesJson)
                    NormalizePath = FileSystem.joinAndNormalisePath(FolderPackagesJson, Path)
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
        if self.project.pathToConfigsJson is not None:
            baseName = FileSystem.getBasename(self.project.pathToConfigsJson)
            newJsonPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite configs json %s" % newJsonPath)
            self.project.configsJson.write(newJsonPath)
            pass

        #credentials
        if self.project.pathToCredentialsJson is not None:
            baseName = FileSystem.getBasename(self.project.pathToCredentialsJson)
            newJsonPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite credentials json %s" % newJsonPath)
            self.project.credentialsJson.write(newJsonPath)

            secureValue = self.project.secureValue or "0123456789A"

            if OSSystem.tool("Ravinggen", "--in", self.project.pathToCredentialsJson, "--out", newJsonPath, "--secure", secureValue) is False:
                return False
                pass
            pass

        #packages
        if self.project.pathToPackagesJson is not None:
            baseName = FileSystem.getBasename(self.project.pathToPackagesJson)
            newJsonPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite packages json %s" % newJsonPath)
            self.project.packagesJson.write(newJsonPath)
            pass

        #settings
        if self.project.pathToSettingsJson is not None:
            baseName = FileSystem.getBasename(self.project.pathToSettingsJson)
            newJsonPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, baseName)
            ErrorHandler.importantMessage("Rewrite packages json %s" % newJsonPath)
            self.project.settingsJson.write(newJsonPath)
            pass

        #Application
        iniName = FileSystem.getBasename(self.project.pathToApplicationJson)
        newJsonPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, iniName)

        #Set new path to root of the project
        # ? without arr = list() a string will be written into applicationConfig
        if self.project.pathToConfigsJson is not None:
            arr = list()
            arr.append(FileSystem.getBasename(self.project.pathToConfigsJson))
            self.project.applicationConfig["Configs"]["Path"] = arr
            pass

        if self.project.pathToCredentialsJson is not None:
            arr = list()
            arr.append(FileSystem.getBasename(self.project.pathToCredentialsJson))
            self.project.applicationConfig["Credentials"]["Path"] = arr
            pass

        if self.project.pathToPackagesJson is not None:
            arr = list()
            arr.append(FileSystem.getBasename(self.project.pathToPackagesJson))
            self.project.applicationConfig["Packages"]["Path"] = arr
            pass

        if self.project.pathToSettingsJson is not None:
            arr = list()
            arr.append(FileSystem.getBasename(self.project.pathToSettingsJson))
            self.project.applicationConfig["Settings"]["Path"] = arr

            for Path in self.project.settingPaths:
                SourcePath = FileSystem.joinAndNormalisePath(self.project.sourceDir, Path)
                DestinationPath = FileSystem.joinAndNormalisePath(self.project.destinationDir, Path)

                FileSystem.copyFile(SourcePath, DestinationPath)
                pass
            pass

        ErrorHandler.importantMessage("Rewrite application json %s"%newJsonPath)
        self.project.applicationConfig.write(newJsonPath)
        pass
    pass
