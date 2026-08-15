from PyBuilder.Config.ConfigJson import ConfigJson
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.FileSystem import FileSystem
from PyBuilder.ResourcePack import ResourcePack

class Project(object):
    def __init__(self):
        super(Project, self).__init__()
        self.applicationConfig = ConfigJson()

        self.configsJson = ConfigJson("Configs.json")
        self.credentialsJson = ConfigJson("Credentials.json")
        self.packagesJson = ConfigJson("Packages.json")
        self.settingsJson = ConfigJson()

        self.projectName = None

        self.pathToApplicationJson = None

        self.pathToConfigsJson = None
        self.pathToCredentialsJson = None
        self.pathToPackagesJson = None
        self.pathToSettingsJson = None

        self.destinationDir = None
        self.sourceDir = None

        self.dirBin2 = None

        self.pathToProtocolXml = None

        self.pathToSourceExe = None
        self.pathToDestinationExe = None
        # self.pathToResources = None

        self.pathToIconGroup = None

        self.oldExeFileName = None
        self.newExeFileName = None
        self.exeFileDescription = None

        self.imageConvertQuality = 100
        self.imageConvertMode = None
        self.imagePremultiply = False
        self.resourceTag = []
        self.extraResourceTag = []
        self.extraPakName = None
        self.extraResourceProcess = False

        self.compilePython = True

        self.removeDestDirIfExist = None

        self.isMetabuf = False

        self.atlasMaxWidth = None
        self.atlasMaxHeight = None
        self.atlasSquare = False
        self.findMinimalAtlasSize = None
        self.logDir = None
        self.secureValue = None

        self.FlvToGvf = None

        self.packs = {}
        self.packNames = []
        self.settingPaths = []
        pass

    def initialise(self):
        if self.loadApplicationJson() is False:
            ErrorHandler.warning("invalid load application json")

            return False
            pass

        if self.loadConfigsJson() is False:
            ErrorHandler.warning("invalid load configs json")

            return False
            pass

        if self.loadCredentialsJson() is False:
            ErrorHandler.warning("invalid load credentials json")

            return False
            pass

        if self.loadPackagesJson() is False:
            ErrorHandler.warning("invalid load packages json")

            return False
            pass

        if self.loadSettingsJson() is False:
            ErrorHandler.warning("invalid load settings json")

            return False
            pass

        return True
        pass

    def loadApplicationJson(self):
        ErrorHandler.importantMessage("Load application.json %s" % self.pathToApplicationJson)

        self.applicationConfig.read(self.pathToApplicationJson)

        self.dirBin2 = FileSystem.getDirname(self.pathToApplicationJson)

        if "Configs" in self.applicationConfig:
            ConfigsPath = self.applicationConfig["Configs"]["Path"][0]
            self.pathToConfigsJson = FileSystem.joinAndNormalisePath(self.dirBin2, ConfigsPath)
            pass

        if "Credentials" in self.applicationConfig:
            CredentialsPath = self.applicationConfig["Credentials"]["Path"][0]
            self.pathToCredentialsJson = FileSystem.joinAndNormalisePath(self.dirBin2, CredentialsPath)
            pass

        if "Packages" in self.applicationConfig:
            PackagesPath = self.applicationConfig["Packages"]["Path"][0]
            self.pathToPackagesJson = FileSystem.joinAndNormalisePath(self.dirBin2, PackagesPath)
            pass

        if "Settings" in self.applicationConfig:
            SettingsPath = self.applicationConfig["Settings"]["Path"][0]
            self.pathToSettingsJson = FileSystem.joinAndNormalisePath(self.dirBin2, SettingsPath)
            pass

        return True
        pass

    def loadConfigsJson(self):
        if self.pathToConfigsJson is None:
            return True
            pass

        ErrorHandler.importantMessage("Load configs %s"%(self.pathToConfigsJson))
        self.configsJson.read(self.pathToConfigsJson)
        self.projectName = self.configsJson["Project"]["Name"]
        self.codeName = self.configsJson["Project"]["Codename"]
        del self.configsJson["Project"]["Codename"]

        return True
        pass

    def loadCredentialsJson(self):
        if self.pathToCredentialsJson is None:
            return True
            pass

        ErrorHandler.importantMessage("Load credentials %s"%(self.pathToCredentialsJson))
        self.credentialsJson.read(self.pathToCredentialsJson)

        return True
        pass

    def createResourcePack(self, params):
        path = params.get("Path", "")
        description = params.get("Description", None)
        basePath = path
        name = params["Name"]

        FontsPath = []
        TextsPath = []

        sourceDirName = FileSystem.joinAndNormalisePath(self.dirBin2, basePath)

        newPath = FileSystem.getRelPath(self.sourceDir, FileSystem.joinAndNormalisePath(
            FileSystem.splitPath(self.pathToPackagesJson)[0], path))
        newPath = FileSystem.addFolderBackslash(newPath)
        destinationDirName = FileSystem.joinAndNormalisePath(self.destinationDir, newPath)

        if description is None:
            return ResourcePack(self, name, None, self.destinationDir, sourceDirName, destinationDirName)

        extension = FileSystem.getFileExtension(description)

        if extension == "bin":
            params["Format"] = "bin"
            filename = FileSystem.setFileExtension(description, "xml")
            pack = ResourcePack(self, name, filename, self.destinationDir, sourceDirName, destinationDirName)
            return pack

        if extension in ("json", "xml"):
            if self.isMetabuf is True:
                params["Description"] = FileSystem.setFileExtension(description, "bin")
                params["Format"] = "bin"

            pack = ResourcePack(self, name, description, self.destinationDir, sourceDirName, destinationDirName)
            return pack

        ErrorHandler.error("package '%s' Description must be JSON, XML or BIN: %s" % (name, description))
        return None

        pass

    def loadPackagesJson(self):
        if self.pathToPackagesJson is None:
            return True
            pass

        ErrorHandler.importantMessage("Load Packages %s" %(self.pathToPackagesJson))

        pathToPackagesJson = self.pathToPackagesJson
        self.packagesJson.read(pathToPackagesJson)

        if "GAME_PACKAGES" not in self.packagesJson:
            ErrorHandler.error ("You must determine GAME_PACKAGES in Packages.json")
            return False
            pass

        ErrorHandler.importantMessage("Collecting resource packs information")

        GameResources = self.packagesJson["GAME_PACKAGES"]
        #FIXME
        if "FrameworkPack" in GameResources:
            packNames = []
            FrameworkPackNames = GameResources["FrameworkPack"]
            if isinstance(FrameworkPackNames, str) is True:
                packNames.append(FrameworkPackNames)
                pass
            else:
                packNames += FrameworkPackNames
                pass

            self.createPacks(packNames)
            self.packNames.extend(packNames)
            pass

        if "ResourcePack" in GameResources:
            packNames = []
            ResourcePackNames = GameResources["ResourcePack"]
            if isinstance(ResourcePackNames, str) is True:
                packNames.append(ResourcePackNames)
                pass
            else:
                packNames += ResourcePackNames
                pass

            self.createPacks(packNames)
            self.packNames.extend(packNames)
            pass

        if "LanguagePack" in GameResources:
            packNames = []
            LanguagePackNames = GameResources["LanguagePack"]
            if isinstance(LanguagePackNames, str) is True:
                packNames.append(LanguagePackNames)
                pass
            else:
                packNames += LanguagePackNames
                pass

            self.createPacks(packNames)
            self.packNames.extend(packNames)
            pass

        return True
        pass

    def loadSettingsJson(self):
        if self.pathToSettingsJson is None:
            return True
            pass

        ErrorHandler.importantMessage("Load Settings %s" %(self.pathToSettingsJson))

        pathToSettingsJson = self.pathToSettingsJson
        self.settingsJson.read(pathToSettingsJson)

        if "GAME_SETTINGS" not in self.settingsJson:
            ErrorHandler.error("You must determine GAME_SETTINGS")
            return False
            pass

        GAME_SETTINGS = self.settingsJson["GAME_SETTINGS"]

        if "Setting" not in GAME_SETTINGS:
            return True
            pass

        SettingName = GAME_SETTINGS["Setting"]

        settingNames = []
        if isinstance(SettingName, str) is True:
            settingNames.append(SettingName)
            pass
        else:
            settingNames += SettingName
            pass

        for name in settingNames:
            Setting = self.settingsJson[name]

            Path = Setting["Path"]

            self.settingPaths.append(Path)
            pass

        return True
        pass

    def createPacks(self, ResourcePackNames):
        for resourcePackName in ResourcePackNames:
            if resourcePackName not in self.packagesJson:
                ErrorHandler.error( "PakName not defined %s"%(resourcePackName))
                continue
                pass

            section = self.packagesJson[resourcePackName]

            if "Dev" in section and section["Dev"] == "1":
                continue
                pass

            # section["Path"] = FileSystem.getBasename(section["Path"])
            packName = section["Name"]

            if self.hasPack(packName) is True:
               continue
               pass

            pack = self.createResourcePack(section)
            self.addPack(packName, pack)
            pass
        pass

    def getPackageJson(self, packName):
        return self.packagesJson[packName]
        pass

    def addPack(self, packName, pack):
        if pack is None:
            ErrorHandler.error("Unsupported resource pack description %s" % (packName))
            return

        if pack.initialise() is False:
            ErrorHandler.error("Pak init error %s" % (packName))
            return
            pass

        self.packs[packName] = pack
        pass

    def hasPack(self, packName):
        if packName in self.packs:
            return True
            pass

        return False
        pass

    def getPack(self, packName):
        return self.packs[packName]
        pass

    def getPacks(self):
        return self.packs
        pass
    pass
