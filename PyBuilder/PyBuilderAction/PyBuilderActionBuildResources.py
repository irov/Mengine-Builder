from PyBuilder.TagHandler.TagHandlerPool import TagHandlerPool

from PyBuilder.TagHandler.TagHandlerImage import TagHandlerImage
from PyBuilder.TagHandler.TagHandlerResource import TagHandlerResource
from PyBuilder.TagHandler.TagHandlerResources import TagHandlerResources
from PyBuilder.TagHandler.TagHandlerMaterials import TagHandlerMaterials
from PyBuilder.TagHandler.TagHandlerScripts import TagHandlerScripts
from PyBuilder.TagHandler.TagHandlerData import TagHandlerData
from PyBuilder.TagHandler.TagHandlerText import TagHandlerText
from PyBuilder.TagHandler.TagHandlerGlyph import TagHandlerGlyph
from PyBuilder.TagHandler.TagHandlerFont import TagHandlerFont
from PyBuilder.TagHandler.TagHandlerInclude import TagHandlerInclude
from PyBuilder.TagHandler.TagHandlerVertexShader import TagHandlerVertexShader
from PyBuilder.TagHandler.TagHandlerFragmentShader import TagHandlerFragmentShader


from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageCopy import ResourceHandlerImageCopy
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToOGG import ResourceHandlerSoundConvertToOGG
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToAAC import ResourceHandlerSoundConvertToAAC
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToWAV import ResourceHandlerSoundConvertToWAV
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerSoundConvertToMP3 import ResourceHandlerSoundConvertToMP3
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToHit import ResourceHandlerImageConvertToHit
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToWEBP import ResourceHandlerImageConvertToWEBP
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToWEBPAndETC1 import ResourceHandlerImageConvertToWEBPAndETC1
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToETC1 import ResourceHandlerImageConvertToETC1
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToDXT1 import ResourceHandlerImageConvertToDXT1
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerImageConvertToPVRTC import ResourceHandlerImageConvertToPVRTC
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerCursorSystem import ResourceHandlerCursorSystem
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerCursorICO import ResourceHandlerCursorICO
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerFile import ResourceHandlerFile
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerVideo import ResourceHandlerVideo
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerParticle import ResourceHandlerParticle
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerEmitterContainer import ResourceHandlerEmitterContainer
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerSpine import ResourceHandlerSpine
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerMovie2 import ResourceHandlerMovie2
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerMusicConvertToOGG import ResourceHandlerMusicConvertToOGG
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerMusicConvertToAAC import ResourceHandlerMusicConvertToAAC
from PyBuilder.TagHandler.ResourceHandler.ResourceHandlerMusicConvertToMP3 import ResourceHandlerMusicConvertToMP3

from PyBuilder.PyBuilderAction.PyBuilderAction import PyBuilderAction
from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder import Constants

class PyBuilderActionBuildResources(PyBuilderAction):
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
