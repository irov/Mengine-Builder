from Builder.Error.ErrorHandler import ErrorHandler

from Builder.Pack2D.Atlas.Atlas import Atlas
from Builder.Pack2D.Packing2D.Packing2D import Packing2D
from Builder.Pack2D.Packing2D.Bin import Bin

class AtlasGenerator(object):
    def __init__(self):
        super(AtlasGenerator, self).__init__()
        self.packing = Packing2D()
        pass

    def initialise(self, settings, dirPath, relativeFileName, texMode, atlasType, fillColor):
        self.dirPath = dirPath
        self.relativeFileName = relativeFileName

        self.settings = settings
        self.texMode = texMode
        self.atlasType = atlasType
        self.fillColor = fillColor

        self.images = {}
        self.images2 = {}
        self.images3 = {}
        self.wastedImages = []
        self.atlases = []

        self.packing.initialise(settings)
        pass

    def getAtlasNames(self):
        atlasNames = []

        for atlas in self.atlases:
            fileName = atlas.getFileName()
            atlasNames.append(fileName)
            pass

        return atlasNames
        pass

    def getNewAtlas(self, binSet):
        index = len(self.atlases)
        counter = "%i" % index

        atlas = Atlas()
        atlasFileName = self.relativeFileName + "_atlas_" +counter + "." + self.atlasType
        binWidth = binSet.getWidth()
        binHeight = binSet.getHeight()
        atlas.initialise(binWidth, binHeight, self.dirPath, atlasFileName, self.texMode, self.atlasType, self.fillColor)
        return atlas
        pass

    def addImages(self, images):
        for image in images:
            self.addImage(image)
            pass
        pass

    def addImage(self, image):
        if image.path in self.images2:
            idBin = self.images2[image.path]

            if idBin not in self.images3:
                self.images3[idBin] = []
                pass

            self.images3[idBin].append(image)
            return
            pass

        width = image.getWidth()
        height = image.getHeight()
        bin = Bin(0, 0, width, height)
        idBin = len(self.images)
        bin.setId(idBin)
        self.packing.push(bin)

        self.images[idBin] = image
        self.images2[image.path] = idBin
        pass

    def _workWithWaste(self, wasted):
        for wasteImage in wasted:
            image = self._getImageForBin(wasteImage)
            self.wastedImages.append(image)
            pass
        pass

    def _getImageForBin(self, bin):
        idBin = bin.getId()
        image = self.images[idBin]
        return image
        pass

    def _getImage2ForBin(self, bin):
        idBin = bin.getId()
        if idBin not in self.images3:
            return []
            pass

        images = self.images3[idBin]

        return images
        pass

    def _workWithResult(self, binSets):
        for binSet in binSets:
            if binSet.empty() is True:
                continue
                pass

            bin_images = []
            atlas = self.getNewAtlas(binSet)

            for bin in binSet:
                image = self._getImageForBin(bin)

                image.setBin(bin)
                atlas.addImage(image)
                bin_images.append(image)

                images = self._getImage2ForBin(bin)

                for image2 in images:
                    image2.setBin(bin)
                    atlas.addImage2(image2)
                    pass
                pass

            atlas.pack()
            # atlas.crop()
            if atlas.save() is False:
                ErrorHandler.warning("invalid atlas save [%s]", self.__repr__())

                return False
                pass

            if self.settings.isDebug is True:
                #atlas.show()
                pass

            self.atlases.append(atlas)

            #print("Atlas file name:")
            #print(atlas.getFileName())
            #print("Images in this atlas:")
            #for im in bin_images:
            #    print(im.getImagePath())

            atlas.finalize()

            pass

        return True
        pass

    def report(self, binSets):
        if len(binSets) == 0:
            return
            pass

        total = 0
        for binSet in binSets:
            total += binSet.getEfficiency()
            pass

        middle = total / len(binSets)
        #print ("Count images: %i efficiency : %4.2f " % (len(binSets), middle) )
        pass

    def generate(self):
        self.packing.pack()

        wasted = self.packing.getWaste()
        self._workWithWaste(wasted)

        binSets = self.packing.getResult()

        if self._workWithResult(binSets) is False:
            ErrorHandler.warning("invalid atlas generator result [%s]", self.__repr__())

            return False
            pass

        if self.settings.isDebug is True:
            self.report(binSets)
            pass
        pass


    def getWastedImages(self):
        return self.wastedImages
        pass
    pass
