from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Atlas.ResourceCollector.ResourceCollector import ResourceCollector
from Builder.FileSystem import FileSystem
from Builder.Watcher.Watcher import Watcher
from Builder import Constants
from Builder.Environment import Environment
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.Constants import ATLAS_TEXTURE_BORDER_SIZE
from Builder.Pack2D.Atlas.AtlasGenerator import AtlasGenerator
from Builder.Pack2D.Packing2D.PackingSettings import PackingSettings
from Builder.Pack2D.Packing2D import GuillotineSplitRule, BinSizeMode, BorderMode,\
    PackingAlgorithm, PackingMode, PlaceHeuristic, SortKey, SortOrder, RotateMode,BorderType


from Builder.Pack2D.Packing2D.Border import Border


class BuilderActionMakeAtlas(BuilderAction):
    def collectPacks(self):
        packs = self.project.getPacks()
        for packName, pack in packs.items():
            collector = ResourceCollector(self.project)

            if collector.collect(pack) is False:
                ErrorHandler.warning("invalid collect pack [%s] pack [%s]", self.__repr__(), packName)
                return False

            if self.createAtlas(collector, pack) is False:
                ErrorHandler.warning("invalid create atlas [%s] pack [%s]", self.__repr__(), packName)
                return False
                pass
            pass

        return True
        pass

    def _onRun(self):
        self.alreadyInAtlasResources = []

        Watcher.startInterval("MakeAtlas")
        result = self.collectPacks()
        Watcher.stopInterval("MakeAtlas")

        return result
        pass

    def getAtlasPathForSection(self, section, pack):
        name = "Atlas/" + section.getName()

        project = Environment.getCurrentProject()
        packDir = project.logDir
        # packDir = pack.getSourceDir()
        return (packDir,name)
        pass

    def packResources(self, generator, resources, duplicate):
        for resource in resources:
            if duplicate is False and resource.isAlreadyInAtlas():
                if resource not in self.alreadyInAtlasResources:
                    self.alreadyInAtlasResources.append(resource)
                    pass
                continue
                pass

            type = resource.getType()


            if type == "ResourceExternal":
                resourcesExternal = resource.getImageResources()
                self.packResources(generator, resourcesExternal, duplicate)
                pass
            elif type == "ResourceImageDefault":
                image = resource.getImage()
                if image is None:
                    continue
                    pass

                generator.addImage(image)
                pass
            pass
        pass

    def createAtlas(self, collector, pack):
        settings = PackingSettings()

        settings.packingAlgorithm = PackingAlgorithm.MAX_RECTANGLES
        settings.placeHeuristic = PlaceHeuristic.BOTTOM_LEFT
        settings.sortOrder = SortOrder.DESC
        settings.sortKey =  SortKey.LONGER_SIDE

        if self.project.findMinimalAtlasSize is True:
            if self.project.atlasSquare is False:
                settings.binSizeMode = BinSizeMode.MINIMIZE_POW2_MINIMIZE_LAST
                pass
            else:
                settings.binSizeMode = BinSizeMode.MINIMIZE_POW2_SQUARE_MINIMIZE_LAST
                pass
            pass
        else:
            if self.project.atlasSquare is False:
                settings.binSizeMode = BinSizeMode.MINIMIZE_POW2
                pass
            else:
                settings.binSizeMode = BinSizeMode.MINIMIZE_POW2_SQUARE
                pass
            pass

        settings.packingMode = PackingMode.OFFLINE
        settings.packingAlgorithmAbility = None
        settings.rotateMode = RotateMode.SIDE_WAYS

        settings.maxWidth = self.project.atlasMaxWidth
        settings.maxHeight = self.project.atlasMaxHeight
        settings.border = Border(bbox=(1, 1, 1, 1), type=BorderType.PIXELS_FROM_EDGE, color=(220,128,13))
        settings.borderMode = BorderMode.AUTO
        settings.isDebug = True
        settings.borderSize = ATLAS_TEXTURE_BORDER_SIZE
        settings.splitRule = GuillotineSplitRule.MIN_AREA

        tags = collector.getTags()
        for section in tags.values():
            print("###########################tags", section.getName())
            atlasPathData = self.getAtlasPathForSection(section, pack)

            directory = FileSystem.getDirname(FileSystem.joinPath(atlasPathData[0], atlasPathData[1]))
            FileSystem.makeDirsRecursiveIfNotExist(directory)

            generator = AtlasGenerator()
            generator.initialise(settings, atlasPathData[0], atlasPathData[1], Constants.ATLAS_TEXTURE_TYPE, Constants.ATLAS_IMAGE_TYPE, Constants.ATLAS_FILL_COLOR)

            items = section.getItems()
            self.packResources(generator, items, True)

            if generator.generate() is False:
                ErrorHandler.warning("invalid generate atlas [%s] path [%s]", self.__repr__(), atlasPathData)
                return False
                pass

            wasted = generator.getWastedImages()
            for waste in wasted:
                ErrorHandler.error("AtlasGenerator can`t  pack image %s" % waste)
                continue
                pass
            pass

        sections = collector.getSections()
        for section in sections:
            print("###########################section", section.getName())
            atlasPathData = self.getAtlasPathForSection(section, pack)

            directory = FileSystem.getDirname(FileSystem.joinPath(atlasPathData[0], atlasPathData[1]))
            FileSystem.makeDirsRecursiveIfNotExist(directory)

            generator = AtlasGenerator()
            generator.initialise(settings, atlasPathData[0], atlasPathData[1], Constants.ATLAS_TEXTURE_TYPE, Constants.ATLAS_IMAGE_TYPE, Constants.ATLAS_FILL_COLOR)

            items = section.getItems()
            self.packResources(generator, items, False)

            if generator.generate() is False:
                ErrorHandler.warning("invalid generate atlas [%s] path [%s]", self.__repr__(), atlasPathData)
                return False
                pass

            wasted = generator.getWastedImages()
            for waste in wasted:
                ErrorHandler.error("AtlasGenerator can`t  pack image %s" % waste)
                continue
                pass
            pass

        return True
        pass

    def _onFinalise(self):
        pass
