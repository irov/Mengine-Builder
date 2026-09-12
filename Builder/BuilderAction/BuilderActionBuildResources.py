from Builder.TagHandler.TagHandlerPool import TagHandlerPool

from Builder.TagHandler.TagHandlerImage import TagHandlerImage
from Builder.TagHandler.TagHandlerResource import TagHandlerResource
from Builder.TagHandler.TagHandlerResources import TagHandlerResources
from Builder.TagHandler.TagHandlerMaterials import TagHandlerMaterials
from Builder.TagHandler.TagHandlerScripts import TagHandlerScripts
from Builder.TagHandler.TagHandlerData import TagHandlerData
from Builder.TagHandler.TagHandlerText import TagHandlerText
from Builder.TagHandler.TagHandlerGlyph import TagHandlerGlyph
from Builder.TagHandler.TagHandlerFont import TagHandlerFont
from Builder.TagHandler.TagHandlerInclude import TagHandlerInclude
from Builder.TagHandler.TagHandlerVertexShader import TagHandlerVertexShader
from Builder.TagHandler.TagHandlerFragmentShader import TagHandlerFragmentShader


from Builder.TagHandler.ResourceHandler.ResourceHandlerImageCopy import ResourceHandlerImageCopy
from Builder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToOGG import ResourceHandlerSoundConvertToOGG
from Builder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToAAC import ResourceHandlerSoundConvertToAAC
from Builder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToWAV import ResourceHandlerSoundConvertToWAV
from Builder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToMP3 import ResourceHandlerSoundConvertToMP3
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToHit import ResourceHandlerImageConvertToHit
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToWEBP import ResourceHandlerImageConvertToWEBP
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToWEBPAndETC1 import ResourceHandlerImageConvertToWEBPAndETC1
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToETC1 import ResourceHandlerImageConvertToETC1
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToDXT1 import ResourceHandlerImageConvertToDXT1
from Builder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToPVRTC import ResourceHandlerImageConvertToPVRTC
from Builder.TagHandler.ResourceHandler.ResourceHandlerCursorSystem import ResourceHandlerCursorSystem
from Builder.TagHandler.ResourceHandler.ResourceHandlerCursorICO import ResourceHandlerCursorICO
from Builder.TagHandler.ResourceHandler.ResourceHandlerFile import ResourceHandlerFile
from Builder.TagHandler.ResourceHandler.ResourceHandlerTiledMap import ResourceHandlerTiledMap
from Builder.TagHandler.ResourceHandler.ResourceHandlerVideo import ResourceHandlerVideo
from Builder.TagHandler.ResourceHandler.ResourceHandlerParticle import ResourceHandlerParticle
from Builder.TagHandler.ResourceHandler.ResourceHandlerEmitterContainer import ResourceHandlerEmitterContainer
from Builder.TagHandler.ResourceHandler.ResourceHandlerSpine import ResourceHandlerSpine
from Builder.TagHandler.ResourceHandler.ResourceHandlerMovie2 import ResourceHandlerMovie2
from Builder.TagHandler.ResourceHandler.ResourceHandlerMusicConvertToOGG import ResourceHandlerMusicConvertToOGG
from Builder.TagHandler.ResourceHandler.ResourceHandlerMusicConvertToAAC import ResourceHandlerMusicConvertToAAC
from Builder.TagHandler.ResourceHandler.ResourceHandlerMusicConvertToMP3 import ResourceHandlerMusicConvertToMP3

from Builder.BuilderAction.BuilderAction import BuilderAction
from Builder.Error.ErrorHandler import ErrorHandler
from Builder import Constants

class BuilderActionBuildResources(BuilderAction):
    def getResourcesPool(self):
        resourcesPool = TagHandlerPool(self.project)

        imageConvertMode = self.project.imageConvertMode

        if imageConvertMode == Constants.IMAGE_MODE_CONVERT_NO_CONVERT:
            resourcesPool.setHandler("ResourceImageDefault", ResourceHandlerImageCopy())
            pass
        elif imageConvertMode == Constants.IMAGE_MODE_CONVERT_PNG_TO_WEBP:
            resourcesPool.setHandler("ResourceImageDefault", ResourceHandlerImageConvertToWEBP())
            pass
        elif imageConvertMode == Constants.IMAGE_MODE_CONVERT_PNG_TO_WEBP_AND_ETC1:
            resourcesPool.setHandler("ResourceImageDefault", ResourceHandlerImageConvertToWEBPAndETC1())
            pass
        elif imageConvertMode == Constants.IMAGE_MODE_CONVERT_PNG_TO_ETC1:
            resourcesPool.setHandler("ResourceImageDefault", ResourceHandlerImageConvertToETC1())
            pass
        elif imageConvertMode == Constants.IMAGE_MODE_CONVERT_PNG_TO_DXT1:
            resourcesPool.setHandler("ResourceImageDefault", ResourceHandlerImageConvertToDXT1())
            pass
        elif imageConvertMode == Constants.IMAGE_MODE_CONVERT_PNG_TO_PVRTC:
            resourcesPool.setHandler("ResourceImageDefault", ResourceHandlerImageConvertToPVRTC())
            pass
        else:
            ErrorHandler.importantMessage("!!!!!!!!!!!!!!invalid image convert mode!!!!!!!!!!!!!!!!!!")
            pass

        resourcesPool.setHandler("ResourceFile", ResourceHandlerFile())
        resourcesPool.setHandler("ResourceTiledMap", ResourceHandlerTiledMap())

        resourcesPool.setHandler("ResourceParticle", ResourceHandlerParticle())
        resourcesPool.setHandler("ResourceAstralax", ResourceHandlerParticle())
        resourcesPool.setHandler("ResourceEmitterContainer", ResourceHandlerEmitterContainer())
        resourcesPool.setHandler("ResourceVideo", ResourceHandlerVideo())
        resourcesPool.setHandler("ResourceSpine", ResourceHandlerSpine())
        resourcesPool.setHandler("ResourceMovie2", ResourceHandlerMovie2())

        soundConvertMode = self.project.soundConvertMode
        if soundConvertMode == Constants.SOUND_MODE_CONVERT_TO_OGG:
            resourcesPool.setHandler("ResourceSound", ResourceHandlerSoundConvertToOGG())
            pass
        elif soundConvertMode == Constants.SOUND_MODE_CONVERT_TO_AAC:
            resourcesPool.setHandler("ResourceSound", ResourceHandlerSoundConvertToAAC())
            pass
        elif soundConvertMode == Constants.SOUND_MODE_CONVERT_TO_WAV:
            resourcesPool.setHandler("ResourceSound", ResourceHandlerSoundConvertToWAV())
            pass
        elif soundConvertMode == Constants.SOUND_MODE_CONVERT_TO_MP3:
            resourcesPool.setHandler("ResourceSound", ResourceHandlerSoundConvertToMP3())
            pass
        else:
            ErrorHandler.importantMessage("!!!!!!!!!!!!!!invalid sound convert mode!!!!!!!!!!!!!!!!!!")
            pass

        resourcesPool.setHandler("ResourceCursorSystem", ResourceHandlerCursorSystem())
        resourcesPool.setHandler("ResourceCursorICO", ResourceHandlerCursorICO())
        resourcesPool.setHandler("ResourceHIT", ResourceHandlerImageConvertToHit())


        musicConvertMode = self.project.musicConvertMode
        if musicConvertMode == Constants.MUSIC_MODE_CONVERT_TO_OGG:
            resourcesPool.setHandler("ResourceMusic", ResourceHandlerMusicConvertToOGG())
            pass
        elif musicConvertMode == Constants.MUSIC_MODE_CONVERT_TO_AAC:
            resourcesPool.setHandler("ResourceMusic", ResourceHandlerMusicConvertToAAC())
            pass
        elif musicConvertMode == Constants.MUSIC_MODE_CONVERT_TO_MP3:
            resourcesPool.setHandler("ResourceMusic", ResourceHandlerMusicConvertToMP3())
            pass
        else:
            ErrorHandler.importantMessage("!!!!!!!!!!!!!!invalid music convert mode!!!!!!!!!!!!!!!!!!")
            pass

        return resourcesPool
        pass

    def getPool(self):
        resourcesPool = self.getResourcesPool()

        pool = TagHandlerPool(self.project)

        pool.setHandler("Resource", TagHandlerResource(resourcesPool))
        pool.setHandler("Resources", TagHandlerResources())
        pool.setHandler("Materials", TagHandlerMaterials())

        pool.setHandler("Scripts", TagHandlerScripts())
        pool.setHandler("Data", TagHandlerData())
        pool.setHandler("VertexShader", TagHandlerVertexShader())
        pool.setHandler("FragmentShader", TagHandlerFragmentShader())

        pool.setHandler("Text", TagHandlerText())
        pool.setHandler("Image", TagHandlerImage())
        pool.setHandler("Glyph", TagHandlerGlyph())
        pool.setHandler("Font", TagHandlerFont())

        pool.setHandler("Include", TagHandlerInclude())

        return pool
        pass

    def getExtraPool(self):
        resourcesPool = self.getResourcesPool()

        pool = TagHandlerPool(self.project)

        pool.setHandler("Resource", TagHandlerResource(resourcesPool))
        pool.setHandler("Resources", TagHandlerResources())
        pool.setHandler("Include", TagHandlerInclude())

        return pool
        pass

    def _onRun(self):
        ErrorHandler.importantMessage("================Building resources================")

        defaultPool = self.getPool()
        extraPool = self.getExtraPool()

        packs = self.project.getPacks()

        for packName, pack in packs.items():
            ErrorHandler.importantMessage("parsing resource pack %s"%packName)
            if pack.visit(defaultPool) is False:
                ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())
                return False

            if len(self.project.extraResourceTag) != 0:
                ErrorHandler.importantMessage("parsing resource extra pack %s"%packName)
                self.project.extraResourceProcess = True
                if pack.visit(extraPool) is False:
                    ErrorHandler.warning("invalid visit pool [%s]", self.__repr__())
                    return False
                self.project.extraResourceProcess = False
                pass

            if pack.finalise() is False:
                ErrorHandler.warning("invalid finalise resource pack [%s]", packName)
                return False

            pass

        return True
        pass
    pass
