from Builder.Builder import Builder
from Builder.Project import Project
from Builder.Watcher.Watcher import Watcher
from Builder.Error.ErrorHandler import ErrorHandler

def configureBuilderActions(builder, project):
    from Builder.BuilderAction.BuilderActionBuildResources import BuilderActionBuildResources
    from Builder.BuilderAction.BuilderActionChangeJsonConfig import BuilderActionChangeJsonConfig
    from Builder.BuilderAction.BuilderActionCopyExe import BuilderActionCopyExe
    from Builder.BuilderAction.BuilderActionCreatePacks import BuilderActionCreatePacks
    from Builder.BuilderAction.BuilderActionPngOptimize import BuilderActionPngOptimize
    from Builder.BuilderAction.BuilderActionPngResizer import BuilderActionPngResizer
    from Builder.BuilderAction.BuilderActionReports import BuilderActionReports
    from Builder.BuilderAction.BuilderActionXlsxExport import BuilderActionXlsxExport
    from Builder.BuilderAction.BuilderActionMakeAtlas import BuilderActionMakeAtlas
    from Builder.BuilderAction.BuilderActionZipout import BuilderActionZipout
    # from Builder.BuilderAction.BuilderActionCompressAtlas import BuilderActionCompressAtlas

    ####INIT BUILD ACTIONS
    if project.OnlyExe is True:
        builder.addAction(BuilderActionCopyExe())

        if project.Zipout is not None:
            builder.addAction(BuilderActionZipout())
            pass

        return
        pass

    if project.IsXlsxExport is True:
        builder.addAction(BuilderActionXlsxExport())
        pass

    builder.addAction(BuilderActionChangeJsonConfig())

    if project.NoExe is False:
        builder.addAction(BuilderActionCopyExe())
        pass

    if project.IsPngOptimize is True or project.imagePremultiply is True:
        builder.addAction(BuilderActionPngOptimize())
        pass

    if project.IsMakeAtlas is True:
        builder.addAction(BuilderActionMakeAtlas())
        pass

    if project.IsHalfTextures is True:
        builder.addAction(BuilderActionPngResizer())
        pass

    # builder.addAction(BuilderActionCompressAtlas())

    builder.addAction(BuilderActionBuildResources())

    if project.IsCreatePacks is True:
        builder.addAction(BuilderActionCreatePacks())
        pass

    builder.addAction(BuilderActionReports())

    if project.Zipout is not None:
        builder.addAction(BuilderActionZipout())
        pass
    pass

def configureOperations(project):
    from Builder.Operation.OperationFactory import OperationFactory

    OperationFactory.setProject(project)

    from Builder.Operation.OperationCompilePyFile import OperationCompilePyFile
    from Builder.Operation.OperationConvertFFMPEGtoOGG import OperationConvertFFMPEGtoOGG
    from Builder.Operation.OperationConvertFFMPEGtoAAC import OperationConvertFFMPEGtoAAC
    from Builder.Operation.OperationConvertFFMPEGtoWAV import OperationConvertFFMPEGtoWAV
    from Builder.Operation.OperationConvertFFMPEGtoMP3 import OperationConvertFFMPEGtoMP3
    from Builder.Operation.OperationConvertFFMPEGtoWEBM import OperationConvertFFMPEGtoWEBM
    from Builder.Operation.OperationConvertFFMPEGtoOGV import OperationConvertFFMPEGtoOGV
    from Builder.Operation.OperationConvertFFMPEGtoOGVA import OperationConvertFFMPEGtoOGVA
    from Builder.Operation.OperationConvertFFMPEGtoGVF import OperationConvertFFMPEGtoGVF
    from Builder.Operation.OperationResizeVideo import OperationResizeVideo
    from Builder.Operation.OperationCopyHitFile import OperationCopyHitFile
    from Builder.Operation.OperationConvertImageToRGB import OperationConvertImageToRGB
    from Builder.Operation.OperationConvertImageToWEBP import OperationConvertImageToWEBP
    from Builder.Operation.OperationConvertImageToHTF import OperationConvertImageToHTF
    from Builder.Operation.OperationConvertImageToACF import OperationConvertImageToACF
    from Builder.Operation.OperationConvertImageToPVR import OperationConvertImageToPVR
    from Builder.Operation.OperationConvertImageToDDS import OperationConvertImageToDDS
    from Builder.Operation.OperationConvertMetabuf import OperationConvertMetabuf
    from Builder.Operation.OperationCompileMengineEditorAsset import OperationCompileMengineEditorAsset
    from Builder.Operation.OperationCopyDirRecursive import OperationCopyDirRecursive
    from Builder.Operation.OperationCopyFile import OperationCopyFile
    from Builder.Operation.OperationCreateZipPack import OperationCreateZipPack
    from Builder.Operation.OperationPngOptimize import OperationPngOptimize
    from Builder.Operation.OperationCompressPyoFile import OperationCompressPyoFile
    from Builder.Operation.OperationZipDDSFile import OperationZipDDSFile

    from Builder.Operation.OperationRemoveDirRecursive import OperationRemoveDirRecursive
    from Builder.Operation.OperationRemoveFile import OperationRemoveFile
    from Builder.Operation.OperationSplitImageOnRGBAndAlpha import OperationSplitImageOnRGBAndAlpha
    from Builder.Operation.OperationCompressImage import OperationCompressImage
    from Builder.Operation.OperationWriteXmlFromDom import OperationWriteXmlFromDom
    from Builder.Operation.OperationXlsxExport import OperationXlsxExport

    from Builder.Operation.OperationRenameFile import OperationRenameFile
    from Builder.Operation.OperationSetExeVersionInfo import OperationSetExeVersionInfo
    from Builder.Operation.OperationYamdiOptimize import OperationYamdiOptimize
    from Builder.Operation.OperationChangeIcons import OperationChangeIcons
    from Builder.Operation.OperationConvertFlvToGvf import OperationConvertFlvToGvf
    from Builder.Operation.OperationConvertText2VSO import OperationConvertText2VSO
    from Builder.Operation.OperationConvertText2PSO import OperationConvertText2PSO
    from Builder.Operation.OperationConvertText2VSO11 import OperationConvertText2VSO11
    from Builder.Operation.OperationConvertText2PSO11 import OperationConvertText2PSO11
    from Builder.Operation.OperationConvertText2Metallib import OperationConvertText2Metallib

    from Builder.Operation.Alias.OperationAliasRewriteXmlFromXmlDomDocument import OperationAliasRewriteXmlFromXmlDomDocument
    from Builder.Operation.Alias.OperationAliasSafetyPngOptimize import OperationAliasSafetyPngOptimize
    from Builder.Operation.Alias.OperationAliasPngResizer import OperationAliasPngResizer

    from Builder.Operation.OperationCopyGlyphs import OperationCopyGlyphs
    from Builder.Operation.OperationCopyFonts import OperationCopyFonts
    from Builder.Operation.OperationCopyTexts import OperationCopyTexts
    from Builder.Operation.OperationAstralaxParse import OperationAstralaxParse

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
    OperationFactory.registerOperationType("CompileMengineEditorAsset", OperationCompileMengineEditorAsset)
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
    builder = Builder()

    builder.initErrorHandler(jsonConfigContent.get("error_reporting"))

    if jsonConfigContent.get("write_logs") is True:
        builder.createLogger(jsonConfigContent.get("log_dir"))
        pass

    project = Project()

    project.logDir = jsonConfigContent.get("log_dir")
    project.pathToApplicationJson = jsonConfigContent.get("path_app_json")
    project.destinationDir = jsonConfigContent.get("dest_dir")
    project.sourceDir = jsonConfigContent.get("path_resources")
    project.pathToSourceExe = jsonConfigContent.get("path_exe_dir")
    project.pathToDestinationExe = jsonConfigContent.get("path_dest_exe_dir")

    project.oldExeFileName = jsonConfigContent.get("old_exe_name")
    project.newExeFileName = jsonConfigContent.get("new_exe_name")
    project.exeFileDescription = jsonConfigContent.get("exe_description")
    project.pathToIconGroup = jsonConfigContent.get("path_icongroup")

    project.isMetabuf = jsonConfigContent.get("metabuf", False)
    project.metabufProtocolPath = jsonConfigContent.get("metabuf_protocol")
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

    configureBuilderActions(builder, project)
    configureOperations(project)

    #############
    if project.initialise() is False:
        ErrorHandler.warning("invalid initialize project")
        return False
        pass

    if builder.initialise(project) is False:
        ErrorHandler.warning("invalid initialize builder")
        return False
        pass

    try:
        if builder.build() is False:
            ErrorHandler.warning("invalid build")
            return False
    finally:
        finalized = builder.finalise()

    if finalized is False:
        ErrorHandler.warning("invalid finalize")
        return False
        pass

    Watcher.printTotal()

    return True
    pass


def build_resource_pack(source_dir, destination_dir, *, description="Package.xml", name="Resources",
                        img_premultiply=False, png_opt=False):
    """Run the normal PNG and resource-export actions into unpublished staging.

    This entry point leaves application/SDK packaging to the caller. It exports
    an image/script resource pack with PNGs retained as PNGs. The full build()
    pipeline additionally supports atlases, resizing and format conversion.
    """
    from pathlib import Path
    import tempfile
    from Builder import Constants
    from Builder.Environment import Environment
    from Builder.ResourcePack import ResourcePack
    from Builder.Toolchain import tool_path
    from Builder.BuilderAction.BuilderActionPngOptimize import BuilderActionPngOptimize
    from Builder.BuilderAction.BuilderActionBuildResources import BuilderActionBuildResources

    source, destination = Path(source_dir).resolve(), Path(destination_dir).resolve()
    if source.is_relative_to(destination) or destination.is_relative_to(source):
        raise ValueError("Resource source and staging directories must not overlap")
    if not source.is_dir() or not (source / description).is_file():
        raise ValueError("Missing resource package: " + str(source / description))
    if type(img_premultiply) is not bool or type(png_opt) is not bool:
        raise ValueError("img_premultiply and png_opt must be booleans")
    if img_premultiply or png_opt:
        tool_path("AlphaSpreading")

    destination.mkdir(parents=True, exist_ok=True)
    previous_project = Environment.getCurrentProject()
    with tempfile.TemporaryDirectory(prefix="resource-build-", dir=destination.parent) as workspace:
        project = Project()
        project.sourceDir, project.destinationDir, project.logDir = str(source), str(destination), workspace
        project.imagePremultiply, project.IsPngOptimize = img_premultiply, png_opt
        project.imageConvertMode = Constants.IMAGE_MODE_CONVERT_NO_CONVERT
        project.soundConvertMode = Constants.SOUND_MODE_CONVERT_TO_OGG
        project.musicConvertMode = Constants.MUSIC_MODE_CONVERT_TO_OGG
        project.isMakeAtlas = False
        project.compilePython = False
        project.platform = None
        builder = Builder()
        builder.initErrorHandler(Constants.ERROR_REPORTING_DEFAULT)
        if img_premultiply or png_opt:
            builder.addAction(BuilderActionPngOptimize())
        builder.addAction(BuilderActionBuildResources())
        builder.project = project
        initialized = []
        try:
            Environment.setCurrentProject(project)
            configureOperations(project)
            pack = ResourcePack(project, name, description, str(source), str(source), str(destination))
            if pack.initialise() is False:
                raise RuntimeError("Cannot read resource package: " + description)
            project.packs = {name: pack}
            for action in builder.actions:
                if action.initialise(builder, project) is False:
                    raise RuntimeError("Cannot initialize resource action: " + str(action))
                initialized.append(action)
            if builder.buildActions() is False:
                raise RuntimeError("Resource build failed: " + description)
        finally:
            for action in reversed(initialized):
                action.finalise()
            ErrorHandler.removeListener(builder.errorListener)
            Environment.setCurrentProject(previous_project)
    return True
