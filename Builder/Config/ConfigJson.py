from functools import reduce

from Builder.Config.BaseConfig import BaseConfig
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem

import re

class ConfigJson(BaseConfig):
    configPath = None
    name = None
    data = None

    def __init__(self, name=None):
        """name - optional parameter for individual processing"""
        super(ConfigJson,self).__init__()

        if name != None:
            self.name = name
            pass

        self.data = {}
        pass

    def read(self, path):
        if FileSystem.isFile(path) is False:
            ErrorHandler.error("ConfigJson file {!r} not found".format(path))
            raise Exception(path)

        self.configPath = path
        self.data = FileSystem.jsonFileLoadContents(path)
        pass

    def deleteUnnecessarySections(self):
        if self.name == None:
            return
            pass

        if self.name.lower() == "packages.json":
            gP = "GAME_PACKAGES"
            sectionsMustExist = reduce(lambda x,y: x + y, self.data.get(gP).values())
            sectionsMustExist.append(gP)
            keys = list(self.data.keys())
            for key in keys:
                if key not in sectionsMustExist:
                    del self.data[key]
                    pass
                pass
            pass
        pass

    def rewritePathsInSection(self, sectionName, packFormat):
        if self.name == None:
            return
            pass

        if self.name.lower() != "packages.json":
            raise BaseException("Unforeseeled situation, refer to the coder. {}".format(self.name))
            pass

        packFormat = packFormat.replace("%s", "")
        self.data[sectionName]["Path"] = self.data[sectionName]["Path"].replace(".", packFormat+".")
        pass

    def _write(self,fp):
        self.deleteUnnecessarySections()
        FileSystem.jsonWriteContentFile(fp, self.data)
        pass
