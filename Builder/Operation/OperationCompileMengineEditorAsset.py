import os
import shutil
import subprocess

from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem
from Builder.Operation.Operation import Operation


class OperationCompileMengineEditorAsset(Operation):
    def _onParams(self, params):
        self.sourcePath = params.pop("SourcePath")
        self.destinationPath = params.pop("DestinationPath")
        self.assetType = params.pop("AssetType")
        self.compilerPath = params.pop("CompilerPath", None)
        pass

    def _getInfo(self):
        return "type %s source %s destination %s" % (
            self.assetType,
            self.sourcePath,
            self.destinationPath,
        )

    def _resolveCompiler(self):
        compiler = self.compilerPath

        if compiler is None:
            compiler = os.environ.get("MENGINE_EDITOR_CLI")
            pass

        if compiler is None:
            compiler = shutil.which("MengineEditorCLI")
            pass

        return compiler

    def _onRun(self):
        if self.assetType not in ("scene", "motion"):
            ErrorHandler.warning("Operation %s failed: unsupported editor asset type %s", self, self.assetType)
            return False

        if FileSystem.isFile(self.sourcePath) is False:
            ErrorHandler.warning("Operation %s failed: source file %s does not exist", self, self.sourcePath)
            return False

        compiler = self._resolveCompiler()

        if compiler is None or FileSystem.isFile(compiler) is False:
            ErrorHandler.warning(
                "Operation %s failed: set MENGINE_EDITOR_CLI to a built MengineEditorCLI executable",
                self,
            )
            return False

        directory = FileSystem.getDirname(self.destinationPath)

        if directory != "" and FileSystem.isDirectory(directory) is False:
            FileSystem.makeDirsRecursive(directory)
            pass

        project_root = os.environ.get("MENGINE_EDITOR_PROJECT_ROOT")
        resource_catalog = os.environ.get("MENGINE_EDITOR_RESOURCE_CATALOG")

        if project_root is None or resource_catalog is None:
            ErrorHandler.warning(
                "Operation %s failed: MENGINE_EDITOR_PROJECT_ROOT and MENGINE_EDITOR_RESOURCE_CATALOG are required for dependency validation",
                self,
            )
            return False

        command = [
            compiler,
            "compile-%s-project" % self.assetType,
            project_root,
            resource_catalog,
            self.sourcePath,
            self.destinationPath,
        ]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if process.returncode != 0:
            ErrorHandler.warning(
                "Operation %s failed with code %s: %s",
                self,
                process.returncode,
                process.stderr.strip(),
            )
            return False

        return True
