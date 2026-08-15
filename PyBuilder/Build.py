from PyBuilder.PyBuilder import PyBuilder
from PyBuilder.Project import Project
from PyBuilder.Watcher.Watcher import Watcher
from PyBuilder.Error.ErrorHandler import ErrorHandler

def configureBuilderActions(pyBuilder, project):
    from PyBuilder.PyBuilderAction.PyBuilderActionBuildResources import PyBuilderActionBuildResources
    from PyBuilder.PyBuilderAction.PyBuilderActionChangeJsonConfig import PyBuilderActionChangeJsonConfig
    from PyBuilder.PyBuilderAction.PyBuilderActionCopyExe import PyBuilderActionCopyExe
    from PyBuilder.PyBuilderAction.PyBuilderActionCreatePacks import PyBuilderActionCreatePacks
    from PyBuilder.PyBuilderAction.PyBuilderActionPngOptimize import PyBuilderActionPngOptimize
    from PyBuilder.PyBuilderAction.PyBuilderActionPngResizer import PyBuilderActionPngResizer
    from PyBuilder.PyBuilderAction.PyBuilderActionReports import PyBuilderActionReports
    from PyBuilder.PyBuilderAction.PyBuilderActionXlsxExport import PyBuilderActionXlsxExport
    from PyBuilder.PyBuilderAction.PyBuilderActionMakeAtlas import PyBuilderActionMakeAtlas
    from PyBuilder.PyBuilderAction.PyBuilderActionZipout import PyBuilderActionZipout
    # from PyBuilder.PyBuilderAction.PyBuilderActionCompressAtlas import PyBuilderActionCompressAtlas

    ####INIT BUILD ACTIONS
    if project.OnlyExe is True:
        pyBuilder.addAction(PyBuilderActionCopyExe())

        if project.Zipout is not None:
            pyBuilder.addAction(PyBuilderActionZipout())
            pass

        return
        pass

    if project.IsXlsxExport is True:
        pyBuilder.addAction(PyBuilderActionXlsxExport())
        pass

    pyBuilder.addAction(PyBuilderActionChangeJsonConfig())

    if project.NoExe is False:
        pyBuilder.addAction(PyBuilderActionCopyExe())
        pass

    if project.IsPngOptimize is True:
        pyBuilder.addAction(PyBuilderActionPngOptimize())
        pass

    if project.IsMakeAtlas is True:
        pyBuilder.addAction(PyBuilderActionMakeAtlas())
        pass

    if project.IsHalfTextures is True:
        pyBuilder.addAction(PyBuilderActionPngResizer())
        pass

    # pyBuilder.addAction(PyBuilderActionCompressAtlas())

    pyBuilder.addAction(PyBuilderActionBuildResources())

    if project.IsCreatePacks is True:
        pyBuilder.addAction(PyBuilderActionCreatePacks())
        pass

    pyBuilder.addAction(PyBuilderActionReports())

    if project.Zipout is not None:
        pyBuilder.addAction(PyBuilderActionZipout())
        pass
    pass

def configureOperations(project):
    from PyBuilder.Operation.OperationFactory import OperationFactory

    OperationFactory.setProject(project)

    from PyBuilder.Operation.OperationCompilePyFile import OperationCompilePyFile
    from PyBuilder.Operation.OperationConvertFFMPEGtoOGG import OperationConvertFFMPEGtoOGG
    from PyBuilder.Operation.OperationConvertFFMPEGtoAAC import OperationConvertFFMPEGtoAAC
    from PyBuilder.Operation.OperationConvertFFMPEGtoWAV import OperationConvertFFMPEGtoWAV
    from PyBuilder.Operation.OperationConvertFFMPEGtoMP3 import OperationConvertFFMPEGtoMP3
    from PyBuilder.Operation.OperationConvertFFMPEGtoWEBM import OperationConvertFFMPEGtoWEBM
    from PyBuilder.Operation.OperationConvertFFMPEGtoOGV import OperationConvertFFMPEGtoOGV
    from PyBuilder.Operation.OperationConvertFFMPEGtoOGVA import OperationConvertFFMPEGtoOGVA
    from PyBuilder.Operation.OperationConvertFFMPEGtoGVF import OperationConvertFFMPEGtoGVF
    from PyBuilder.Operation.OperationResizeVideo import OperationResizeVideo
    from PyBuilder.Operation.OperationCopyHitFile import OperationCopyHitFile
    from PyBuilder.Operation.OperationConvertImageToRGB import OperationConvertImageToRGB
    from PyBuilder.Operation.OperationConvertImageToWEBP import OperationConvertImageToWEBP
    from PyBuilder.Operation.OperationConvertImageToHTF import OperationConvertImageToHTF
    from PyBuilder.Operation.OperationConvertImageToACF import OperationConvertImageToACF
    from PyBuilder.Operation.OperationConvertImageToPVR import OperationConvertImageToPVR
    from PyBuilder.Operation.OperationConvertImageToDDS import OperationConvertImageToDDS
    from PyBuilder.Operation.OperationConvertMetabuf import OperationConvertMetabuf
    from PyBuilder.Operation.OperationCopyDirRecursive import OperationCopyDirRecursive
    from PyBuilder.Operation.OperationCopyFile import OperationCopyFile
    from PyBuilder.Operation.OperationCreateZipPack import OperationCreateZipPack
    from PyBuilder.Operation.OperationPngOptimize import OperationPngOptimize
    from PyBuilder.Operation.OperationCompressPyoFile import OperationCompressPyoFile
    from PyBuilder.Operation.OperationZipDDSFile import OperationZipDDSFile

    from PyBuilder.Operation.OperationRemoveDirRecursive import OperationRemoveDirRecursive
    from PyBuilder.Operation.OperationRemoveFile import OperationRemoveFile
    from PyBuilder.Operation.OperationSplitImageOnRGBAndAlpha import OperationSplitImageOnRGBAndAlpha
    from PyBuilder.Operation.OperationCompressImage import OperationCompressImage
    from PyBuilder.Operation.OperationWriteXmlFromDom import OperationWriteXmlFromDom
    from PyBuilder.Operation.OperationXlsxExport import OperationXlsxExport

    from PyBuilder.Operation.OperationRenameFile import OperationRenameFile
    from PyBuilder.Operation.OperationSetExeVersionInfo import OperationSetExeVersionInfo
    from PyBuilder.Operation.OperationYamdiOptimize import OperationYamdiOptimize
    from PyBuilder.Operation.OperationChangeIcons import OperationChangeIcons
    from PyBuilder.Operation.OperationConvertFlvToGvf import OperationConvertFlvToGvf
    from PyBuilder.Operation.OperationConvertText2VSO import OperationConvertText2VSO
    from PyBuilder.Operation.OperationConvertText2PSO import OperationConvertText2PSO
    from PyBuilder.Operation.OperationConvertText2VSO11 import OperationConvertText2VSO11
    from PyBuilder.Operation.OperationConvertText2PSO11 import OperationConvertText2PSO11
    from PyBuilder.Operation.OperationConvertText2Metallib import OperationConvertText2Metallib

    from PyBuilder.Operation.Alias.OperationAliasRewriteXmlFromXmlDomDocument import OperationAliasRewriteXmlFromXmlDomDocument
    from PyBuilder.Operation.Alias.OperationAliasSafetyPngOptimize import OperationAliasSafetyPngOptimize
    from PyBuilder.Operation.Alias.OperationAliasPngResizer import OperationAliasPngResizer

    from PyBuilder.Operation.OperationCopyGlyphs import OperationCopyGlyphs
    from PyBuilder.Operation.OperationCopyFonts import OperationCopyFonts
    from PyBuilder.Operation.OperationCopyTexts import OperationCopyTexts
    from PyBuilder.Operation.OperationAstralaxParse import OperationAstralaxParse

    OperationFactory.registerOperationType("CompilePyFile", OperationCompilePyFile)
    OperationFactory.registerOperationType("CompressPyoFile", OperationCompressPyoFile)
    OperationFactory.registerOperationType("ZipDDSFile", OperationZipDDSFile)
    OperationFactory.registerOperationType("ConvertFFMPEGtoOGG", OperationConvertFFMPEGtoOGG)
    OperationFactory.registerOperationType("ConvertFFMPEGtoAAC", OperationConvertFFMPEGtoAAC)
    OperationFactory.registerOperationType("ConvertFFMPEGtoWAV", OperationConvertFFMPEGtoWAV)
    OperationFactory.registerOperationType("ConvertFFMPEGtoMP3", OperationConvertFFMPEGtoMP3)
    OperationFactory.registerOperationType("ConvertFFMPEGtoWEBM", OperationConvertFFMPEGtoWEBM)
    OperationFactory.registerOperationType("ConvertFFMPEGtoOGV", OperationConvertFFMPEGtoOGV)
    OperationFactory.registerOperationType("ConvertFFMPEGtoOGVA", OperationConvertFFMPEGtoOGVA)
    OperationFactory.registerOperationType("ConvertFFMPEGtoGVF", OperationConvertFFMPEGtoGVF)

    OperationFactory.registerOperationType("ResizeVideo", OperationResizeVideo)

    OperationFactory.registerOperationType("convertPNGToHIT", OperationCopyHitFile)
    OperationFactory.registerOperationType("ConvertImageToRGB", OperationConvertImageToRGB)
    OperationFactory.registerOperationType("ConvertImageToWEBP", OperationConvertImageToWEBP)
    OperationFactory.registerOperationType("ConvertImageToPVR", OperationConvertImageToPVR)
    OperationFactory.registerOperationType("ConvertImageToDDS", OperationConvertImageToDDS)
    OperationFactory.registerOperationType("ConvertImageToHTF", OperationConvertImageToHTF)
    OperationFactory.registerOperationType("ConvertImageToACF", OperationConvertImageToACF)
    OperationFactory.registerOperationType("ConvertMetabuf", OperationConvertMetabuf)
    OperationFactory.registerOperationType("CopyDirRecursive", OperationCopyDirRecursive)
    OperationFactory.registerOperationType("CopyFile", OperationCopyFile)
    OperationFactory.registerOperationType("CreateZipPack", OperationCreateZipPack)
    OperationFactory.registerOperationType("PngOptimize", OperationPngOptimize)
    OperationFactory.registerOperationType("RemoveDirRecursive", OperationRemoveDirRecursive)
    OperationFactory.registerOperationType("RemoveFile", OperationRemoveFile)
    OperationFactory.registerOperationType("SplitImageOnRGBAndAlpha", OperationSplitImageOnRGBAndAlpha)
    OperationFactory.registerOperationType("CompressImage", OperationCompressImage)
    OperationFactory.registerOperationType("WriteXmlFromDom", OperationWriteXmlFromDom)
    OperationFactory.registerOperationType("XlsxExport", OperationXlsxExport)
    OperationFactory.registerOperationType("YamdiOptimize", OperationYamdiOptimize)
    OperationFactory.registerOperationType("SetExeVersionInfo", OperationSetExeVersionInfo)
    OperationFactory.registerOperationType("RenameFile", OperationRenameFile)
    OperationFactory.registerOperationType("ChangeIcons", OperationChangeIcons)
    OperationFactory.registerOperationType("ConvertFlvToGvf", OperationConvertFlvToGvf)
    OperationFactory.registerOperationType("ConvertText2VSO", OperationConvertText2VSO)
    OperationFactory.registerOperationType("ConvertText2PSO", OperationConvertText2PSO)
    OperationFactory.registerOperationType("ConvertText2VSO11", OperationConvertText2VSO11)
    OperationFactory.registerOperationType("ConvertText2PSO11", OperationConvertText2PSO11)
    OperationFactory.registerOperationType("ConvertText2Metallib", OperationConvertText2Metallib)

    OperationFactory.registerOperationType("CopyGlyphs", OperationCopyGlyphs)
    OperationFactory.registerOperationType("CopyFonts", OperationCopyFonts)
    OperationFactory.registerOperationType("CopyTexts", OperationCopyTexts)
    OperationFactory.registerOperationType("AstralaxParse", OperationAstralaxParse)

    OperationFactory.registerOperationType("AliasSafetyPngOptimize", OperationAliasSafetyPngOptimize)
    OperationFactory.registerOperationType("AliasPngResizer", OperationAliasPngResizer)
    OperationFactory.registerOperationType("AliasRewriteXmlFromXmlDomDocument", OperationAliasRewriteXmlFromXmlDomDocument)

    OperationFactory.registerOperationType("CopyXmlFile", OperationCopyFile)
    pass


def build(jsonConfigContent):
    pyBuilder = PyBuilder()

    pyBuilder.initErrorHandler(jsonConfigContent.get("error_reporting"))

    if jsonConfigContent.get("write_logs") is True:
        pyBuilder.createLogger(jsonConfigContent.get("log_dir"))
        pass

    project = Project()

    project.logDir = jsonConfigContent.get("log_dir")
    project.pathToApplicationJson = jsonConfigContent.get("path_app_json")
    project.pathToProtocolXml = jsonConfigContent.get("path_protocol")

    project.destinationDir = jsonConfigContent.get("dest_dir")
    project.sourceDir = jsonConfigContent.get("path_resources")
    project.pathToSourceExe = jsonConfigContent.get("path_exe_dir")
    project.pathToDestinationExe = jsonConfigContent.get("path_dest_exe_dir")

    project.oldExeFileName = jsonConfigContent.get("old_exe_name")
    project.newExeFileName = jsonConfigContent.get("new_exe_name")
    project.exeFileDescription = jsonConfigContent.get("exe_description")
    project.pathToIconGroup = jsonConfigContent.get("path_icongroup")

    project.isMetabuf = jsonConfigContent.get("metabuf", False)
    project.isMakeAtlas = jsonConfigContent.get("make_atlas")

    project.imageConvertQuality = jsonConfigContent.get("img_convert_quality")
    project.imageConvertMode = jsonConfigContent.get("img_convert")
    project.imagePremultiply = jsonConfigContent.get("img_premultiply")
    project.soundConvertQuality = jsonConfigContent.get("sound_convert_quality")
    project.soundConvertMode = jsonConfigContent.get("sound_convert")
    project.musicConvertQuality = jsonConfigContent.get("music_convert_quality")
    project.musicConvertMode = jsonConfigContent.get("music_convert")
    project.videoConvertQuality = jsonConfigContent.get("video_convert_quality")
    project.videoResize = jsonConfigContent.get("video_resize")

    project.compilePython = jsonConfigContent.get("python_compile")

    project.resourceTag = jsonConfigContent.get("resource_tag")
    project.extraResourceTag = jsonConfigContent.get("extra_resource_tag")
    project.extraPakName = jsonConfigContent.get("extra_pak_name")
    project.removeDestDirIfExist = jsonConfigContent.get("remove_destination_dir_if_exist")
    project.atlasMaxWidth = jsonConfigContent.get("atlas_max_width")
    project.atlasMaxHeight = jsonConfigContent.get("atlas_max_height")
    project.atlasSquare = jsonConfigContent.get("atlas_square")
    project.findMinimalAtlasSize = jsonConfigContent.get("find_minimal_atlas_size")
    project.secureValue = jsonConfigContent.get("secure_value")
    project.FlvToGvf = jsonConfigContent.get("flv_to_gvf")

    project.IsXlsxExport = jsonConfigContent.get("xlsx_export")
    project.IsPngOptimize = jsonConfigContent.get("png_opt")
    project.IsCreatePacks = jsonConfigContent.get("create_packs")
    project.CreatePacksFormat = jsonConfigContent.get("create_packs_format")
    project.CreatePacksLimit = jsonConfigContent.get("create_packs_limit")
    project.IsMakeAtlas = jsonConfigContent.get("make_atlas")
    project.IsHalfTextures = jsonConfigContent.get("half_textures")
    project.NoExe = jsonConfigContent.get("no_exe")
    project.OnlyExe = jsonConfigContent.get("only_exe")
    project.Zipout = jsonConfigContent.get("zipout")

    # project.initialise()

    configureBuilderActions(pyBuilder, project)
    configureOperations(project)

    #############
    if project.initialise() is False:
        ErrorHandler.warning("invalid initialize project")
        return False
        pass

    if pyBuilder.initialise(project) is False:
        ErrorHandler.warning("invalid initialize builder")
        return False
        pass

    if pyBuilder.build() is False:
        ErrorHandler.warning("invalid build")
        return False
        pass

    if pyBuilder.finalise() is False:
        ErrorHandler.warning("invalid finalize")
        return False
        pass

    Watcher.printTotal()

    return True
    pass
