__author__ = 'human88998999877'
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder import Constants
from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction


class PyBuilderActionCreatePacks(PyBuilderAction):
    def convertJsonSectionToPak(self, jsonConfig):
        if "Dev" not in jsonConfig or jsonConfig["Dev"] == "0":
            name = jsonConfig["Name"]
            pakPath = name + "." + Constants.PACK_EXTENSION
            jsonConfig["Path"] = pakPath
            jsonConfig["Type"] = Constants.PACK_TYPE
            pass
        pass

    def _onInitialise(self):
        for resourcePackName in self.project.packNames:
            section = self.project.packagesJson[resourcePackName]
            if "Dev" in section and section["Dev"] == "1":
                continue
                pass

            packName = section["Name"]

            if self.project.hasPack(packName) is False:
                print("self.project.hasPack(packName)")
                ErrorHandler.error("Pack %s not exist" % packName)
                return False
                pass

            pack = self.project.getPack(packName)

            nopak = section.get("NoPak")
            if nopak is not None and nopak == 1:
                pack.setToZip(False)
                continue
                pass

            self.convertJsonSectionToPak(section)

            if pack.isNeedToZip() is False:
                Path = section["Path"]

                zipName = FileSystem.joinAndNormalisePath(self.project.destinationDir, Path)

                pack.setPathToZip(zipName)
                pack.setToZip(True)
                pass
            pass

        return True
        pass

    def _onRun(self):
        ErrorHandler.importantMessage("Creating zip Packs")
        packs = self.project.getPacks()
        for packName, pack in packs.items():
            if pack.isNeedToZip() is False:
                continue
                pass

            if pack.convertDestinationToZip() is False:
                ErrorHandler.error("can`t convert to zip pack %s" % packName)
                return False
                pass

            if pack.removeDestination() is False:
                ErrorHandler.error("can`t remove pack directory %s" % packName)
                return False
                pass
            pass
        pass
    pass
