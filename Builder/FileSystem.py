import os
import os.path
import shutil
import errno
import filecmp
import json

class FileSystem:
    @staticmethod
    def absolutePath(path):
        abspath = os.path.abspath(path)
        return abspath
        pass

    @staticmethod
    def openFile(path,mode):
        file = open(path,mode)
        return file
        pass

    @staticmethod
    def getFileExtension(path):
        pathData = os.path.splitext(path)
        if len(pathData) != 2:
            return None
            pass

        ext = pathData[1]
        ext = ext[1:len(ext)]
        return ext.lower()
        pass

    @staticmethod
    def setFileExtension(path, newExt):
        pathData = os.path.splitext(path)
        if len(pathData) != 2:
            return None
            pass

        basePart =  pathData[0]
        return  basePart + "." + newExt
        pass

    @staticmethod
    def splitByExtension(path):
        pathData = os.path.splitext(path)
        return pathData
        pass

    @staticmethod
    def removeFile(path):
        os.remove(path)
        pass

    @staticmethod
    def normalisePath(path):
        normpath = os.path.normpath(path)
        return normpath
        pass

    @staticmethod
    def getPathDifference(pathLarge, pathSmall):
        pathLargeN = FileSystem.normalisePath(pathLarge)
        pathSmallN = FileSystem.normalisePath(pathSmall)
        pathLargeN.replace(pathSmallN)
        pass

    @staticmethod
    def pathStepBackWard(path, countSteps):
        result = FileSystem.normalisePath(path)

        while True:
            if countSteps <= 0:
                break
                pass

            countSteps -= 1
            result = FileSystem.getDirname(result)
            pass

        return result
        pass

    @staticmethod
    def joinPath(path1,path2):
        path = os.path.join(path1,path2)
        path = os.path.normpath(path)
        return path
        pass

    @staticmethod
    def joinAndNormalisePath(path1,path2):
        path = os.path.join(path1, path2)
        path = os.path.normpath(path)

        return path
        pass

    @staticmethod
    def getRelPath(base, path):
        r = os.path.relpath(path, base)

        return r
        pass

    @staticmethod
    def addFolderBackslash(path):
        r = os.path.join(path, '')
        return r
        pass

    @staticmethod
    def getDirname(path):
        dirname = os.path.dirname(path)

        return dirname
        pass

    @staticmethod
    def getBasename(path):
        basename = os.path.basename(path)

        return basename
        pass

    @staticmethod
    def splitPath(path):
        parts =  os.path.split(path)
        return parts
        pass

    @staticmethod
    def isDirectory(path):
        isDir = os.path.isdir(path)
        return  isDir
        pass

    @staticmethod
    def isFile(path):
        state = os.path.isfile(path)
        return state
        pass

    @staticmethod
    def isAccess(path):
        return os.access(path, os.R_OK)
        pass

    @staticmethod
    def filePutContents(filename,content,mode = "wb"):
        file = open(filename,mode)
        file.write(content)
        file.close()
        pass

    @staticmethod
    def fileGetContents(filename):
        file = open(filename,"r")
        content = file.read()
        file.close()
        return content
        pass

    @staticmethod
    def jsonFileLoadContents(path, withComments=False):
        """Load content from file translations js types to python types"""
        with open(path, 'r', encoding="utf-8") as file:
            try:
                if not withComments:
                    fixed_json = ''.join(line for line in file if not line.replace('\t', '').startswith('//'))
                    json_content = json.loads(fixed_json)
                else:
                    json_content = json.load(file)

            except json.decoder.JSONDecodeError as ex:
                print("invalid load json '{}' error: {}".format(path, ex))
                return None

            except Exception as ex:
                print("while loading '{}' unexpected error {}: {}".format(path, type(ex), ex))
                raise ex

        return json_content

    @staticmethod
    def jsonFileDumpContent(path, jsonContent):
        """Write content on file by path"""
        with open(path, "w") as file:
            json_file = json.dump(jsonContent, file, indent=4)
        return json_file
        pass

    @staticmethod
    def jsonWriteContentFile(fp, jsonContent):
        """Write content in file"""
        json_file = json.dump(jsonContent, fp, indent=4)
        return json_file
        pass

    @staticmethod
    def jsonDumpContent(jsonContent):
        """jsonContent to string"""
        string = json.dumps(jsonContent)
        return string
        pass

    @staticmethod
    def jsonLoadsContent(asJsonContent):
        """asJsonContent(must be string) to dict"""
        jsonContent = json.loads(asJsonContent)
        return jsonContent

    @staticmethod
    def makeDirsRecursiveIfNotExist(path):
        if len(path) == 0:
            return
            pass

        if FileSystem.isDirectory(path) is True:
            return
            pass

        FileSystem.makeDirsRecursive(path)
        pass

    @staticmethod
    def makeDirsRecursive(path):
        os.makedirs(path)
        pass

    @staticmethod
    def makeDir(path):
        os.mkdir(path)
        pass

    @staticmethod
    def isSameFiles(path1,path2):
        state = os.path.samefile(path1,path2)
        return state
        pass

    @staticmethod
    def isEmptyDir(path):
        if len(os.listdir(path)) > 0:
            state = False
        else:
            state = True
        return state
        pass

    @staticmethod
    def getCurrentDirectory():
        curDir = os.getcwd()
        return curDir
        pass

    @staticmethod
    def renameFile(old, new):
        print("old", old)
        print("new", new)
        #os.rename(old,new)
        shutil.move(old, new)
        pass

    @staticmethod
    def copyFile(fileSource, fileDestiny):
        shutil.copy(fileSource,fileDestiny)
        pass

    @staticmethod
    def removeDirRecursive(path):
        shutil.rmtree(path)
        pass

    @staticmethod
    def copyDirRecursive(directorySource, directoryDestiny, copyFileFunction = None, ignorePatterns = None):
        try:
            ignore = shutil.ignore_patterns(ignorePatterns) if ignorePatterns is not None else None
            shutil.copytree(directorySource, directoryDestiny, copy_function=copyFileFunction or shutil.copy2, ignore=ignore, ignore_dangling_symlinks=True, dirs_exist_ok=True)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                if copyFileFunction is not None:
                    copyFileFunction(directorySource, directoryDestiny)
                    pass
                else:
                    shutil.copy(directorySource, directoryDestiny)
                    pass
            else:
                print(
                    'Directory not copied. from %s to %s Error: type %s code %s win %s'
                    % (
                        directorySource,
                        directoryDestiny,
                        type(e),
                        e.errno,
                        getattr(e, "winerror", None),
                    )
                )
                raise
                pass
            pass
        pass

    @staticmethod
    def printTreeDifference(path1, path2):
        checkTrees = filecmp.dircmp(path1, path2)
        checkTrees.report_full_closure()
        pass
    pass
