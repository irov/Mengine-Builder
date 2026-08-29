from Builder.Build import build

from Builder.Arguments.ArgumentInt import ArgumentInt
from Builder.Arguments.ArgumentList import ArgumentList
from Builder.Arguments.ArgumentBool import ArgumentBool
from Builder.Arguments.ArgumentMulti import ArgumentMulti
from Builder.Arguments.ArgumentFloat import ArgumentFloat
from Builder.Arguments.ArgumentString import ArgumentString

from Builder.Error.ErrorHandler import ErrorHandler

import Builder.Constants as Constants
from Builder.FileSystem import FileSystem
from Builder.ConfigLoader import load_build_config

from Builder import Tools

import sys

class BuilderConsoleApp(object):
    def __init__(self):
        super(BuilderConsoleApp,self).__init__()
        self.arguments = []

        class MyLogger:
            def write(self, message):
                Tools.log(message)

            def flush(self):
                pass

        sys.stdout = MyLogger()
        sys.stderr = MyLogger()
        pass

    def addArgument(self,argument):
        self.arguments.append(argument)
        pass

    def fillsConfigArgs(self, jsonContent):
        """fills jsonContent by all arguments and correct values"""
        for argument in self.arguments:
            argInputValue = jsonContent.get(argument.getName())

            if argument.setUpValue(argInputValue) is False:
                ErrorHandler.warning("Failed to set up an argument [%s]", argument.getName())

            jsonContent[argument.getName()] = argument.getValue()
            pass

        return True
        pass

    def help(self):
        info = "MengineBuilder.py -path_config <config.json> [-new_var <name>:<value>]...\nPossible arguments:\n"
        for argument in self.arguments:
            info += argument.getInfo() + "\n"
            pass

        info += "-help - this message"
        print (info)
        pass

    def initialise(self):
        self.addArgument(ArgumentString("path_app_json", "Path to application.json"))
        self.addArgument(ArgumentString("dest_dir", "Path to destination directory"))
        self.addArgument(ArgumentString("path_exe_dir", "Path to directory with *.exe"))
        self.addArgument(ArgumentString("path_dest_exe_dir", "Path where *.exe must be placed"))
        self.addArgument(ArgumentString("path_resources", "Path to directory which contains game resources"))
        self.addArgument(ArgumentInt("img_convert_quality","Image RGBA convert quality"))

        self.addArgument(ArgumentMulti("img_convert", "Image resources convert mode",
            [("convert_to_webp", Constants.IMAGE_MODE_CONVERT_PNG_TO_WEBP),
             ("convert_to_webp_and_etc1", Constants.IMAGE_MODE_CONVERT_PNG_TO_WEBP_AND_ETC1),
             ("convert_to_etc1", Constants.IMAGE_MODE_CONVERT_PNG_TO_ETC1),
             ("convert_to_pvrtc", Constants.IMAGE_MODE_CONVERT_PNG_TO_PVRTC),
             ("convert_to_dxt1", Constants.IMAGE_MODE_CONVERT_PNG_TO_DXT1),
             (False, Constants.IMAGE_MODE_CONVERT_NO_CONVERT )]))

        self.addArgument(ArgumentInt("sound_convert_quality", "Quality for sound", important=False, default=100))

        self.addArgument(ArgumentMulti("sound_convert", "Sound resources convert mode. Possible values: convert_to_ogg, convert_to_aac, convert_to_wav, convert_to_mp3",
            [("convert_to_ogg", Constants.SOUND_MODE_CONVERT_TO_OGG),
             ("convert_to_aac", Constants.SOUND_MODE_CONVERT_TO_AAC),
             ("convert_to_wav", Constants.SOUND_MODE_CONVERT_TO_WAV),
             ("convert_to_mp3", Constants.SOUND_MODE_CONVERT_TO_MP3)]))

        self.addArgument(ArgumentInt("music_convert_quality", "Quality for music", important=False, default=100))

        self.addArgument(ArgumentMulti("music_convert", "Music resources convert mode. Possible values: convert_to_ogg, convert_to_aac, convert_to_mp3",
            [("convert_to_ogg", Constants.MUSIC_MODE_CONVERT_TO_OGG),
             ("convert_to_aac", Constants.MUSIC_MODE_CONVERT_TO_AAC),
             ("convert_to_mp3", Constants.MUSIC_MODE_CONVERT_TO_MP3)]))

        self.addArgument(ArgumentInt("video_convert_quality", "Quality for video", important=False, default=100))

        self.addArgument(ArgumentFloat("video_resize", "Resize video", important=False, default=None))
        self.addArgument(ArgumentBool("img_premultiply", "Premultiply alpha for each image resource", important=False, default=False))
        self.addArgument(ArgumentBool("png_opt", "Use hge png optimizer for each png resource"))
        self.addArgument(ArgumentBool("create_packs", "Packing resources to zip archives"))
        self.addArgument(ArgumentString("create_packs_format", "Packing resources to zip archives [format]", important=False, default="%s%02u%s"))
        self.addArgument(ArgumentInt("create_packs_limit", "Packing resources to zip archives [limit]", important=False, default=-1))
        self.addArgument(ArgumentBool("write_logs", "Logging"))
        self.addArgument(ArgumentString("log_dir", "Directory for writing log. if not specified and -write_logs is set current directory path is used "))

        self.addArgument(ArgumentBool("xlsx_export", "Run Xlsx export from directory with application.json on build start"))
        self.addArgument(ArgumentBool("metabuf", "Converting JSON/XML protocol data to Metabuf BIN"))
        self.addArgument(ArgumentString("old_exe_name", "Name of exe file in path_exe_dir. for example Win32Application.exe"))
        self.addArgument(ArgumentString("new_exe_name", "Wanted exe file name. \"For example Zombie Potatoes in Outer Space.exe\""))
        self.addArgument(ArgumentString("exe_description", "Exe file description"))

        self.addArgument(ArgumentMulti("error_reporting", "Error reporting mode. Possible values: "
                                                    + "default - logged and printed errors, warnings and important messages. "
                                                    + "silent - nothing printed. "
                                                    + "verbose - all printed and logged",
            [("default", Constants.ERROR_REPORTING_DEFAULT),
                ("silent", Constants.ERROR_REPORTING_SILENT),
                ("verbose", Constants.ERROR_REPORTING_VERBOSE)]))

        self.addArgument(ArgumentString("path_icongroup", "Path to icon group file. Usage optional. if not set - icon don`t change ", important=False))
        self.addArgument(ArgumentList("resource_tag", "Attribute of Tag Resources in Pak.xml definitions which means "\
                                            "that only this resources will be exported. Usage Optional. if not set - all resources exported", important=False, default=[]))
        self.addArgument(ArgumentList("extra_resource_tag", "extra_resource_tag", important=False, default=[]))
        self.addArgument(ArgumentString("extra_pak_name", "extra_pak_name", important=False))
        self.addArgument(ArgumentString("secure_value", "used in ravinnger.exe", important=False))

        self.addArgument(ArgumentBool("remove_destination_dir_if_exist", "If True and if exist - removes destination directory"))
        self.addArgument(ArgumentBool("make_atlas", "Pack image resources to atlas."))
        self.addArgument(ArgumentInt("atlas_max_width", "Max width for one atlas", important=False))
        self.addArgument(ArgumentInt("atlas_max_height", "Max height for one atlas", important=False))
        self.addArgument(ArgumentBool("atlas_square", "generate square atlas"))
        self.addArgument(ArgumentBool("flv_to_gvf", "Convert FLV to GVF", important=False))
        self.addArgument(ArgumentBool("find_minimal_atlas_size", "Try to minimize atlas size after pack", important=False))
        self.addArgument(ArgumentBool("half_textures", "half textures", important=False, default=False))
        self.addArgument(ArgumentBool("no_exe", "no exe", important=False, default=False))
        self.addArgument(ArgumentBool("only_exe", "no exe", important=False, default=False))
        self.addArgument(ArgumentString("zipout", "Output zip path", important=False, default=None))
        self.addArgument(ArgumentString("python_compile", "Compile python code", important=False, default=True))
        pass

    def run(self, *args):
        print(args)
        if len(args) == 1:
            if args[0] == "-help":
                self.help()
                return False
                pass
            pass

        if "-path_config" not in args:
            self.help()
            return False
            pass

        index_config = args.index("-path_config") + 1
        buildConfigContent = load_build_config(args[index_config], args)
        self.fillsConfigArgs(buildConfigContent)
        result = build(buildConfigContent)

        return result
        pass
    pass
